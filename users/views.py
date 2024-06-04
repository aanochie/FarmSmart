from datetime import datetime

import bcrypt
from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import current_user, login_user, login_required, logout_user
from markupsafe import Markup
from app import database
from dbSetup import User
from users.forms import RegisterForm, LoginForm, PasswordForm
# Written by: Malak (c2001143)
users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # Check if the current user is anonymous
    if current_user.is_anonymous:
        if form.validate_on_submit():
            # Check if the email is already registered
            user = User.query.filter_by(email=form.email.data).first()

            if user:
                flash("Email already registered")
                return render_template('users/register.html', form=form)

            # Create a new user with the form data
            new_user = User(email=form.email.data,
                            password=form.password.data,
                            firstname=form.firstname.data,
                            lastname=form.lastname.data,
                            role='user')
            database.session.add(new_user)
            database.session.commit()

            session['email'] = new_user.email

            return redirect(url_for('users.setup_2fa'))

    # If the current user is an admin
    elif current_user.role == 'admin':
        if form.validate_on_submit():
            # Check if the email is already registered
            user = User.query.filter_by(email=form.email.data).first()

            if user:
                flash('Email already registered')
                return render_template('users/register.html', form=form)

            # Create a new admin with the form data
            new_admin = User(email=form.email.data,
                             password=form.password.data,
                             firstname=form.firstname.data,
                             lastname=form.lastname.data,
                             role='admin')
            database.session.add(new_admin)
            database.session.commit()

            session['email'] = new_admin.email
            flash('New admin has been registered')
            return redirect(url_for('admin.admin'))

    return render_template('users/register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_anonymous:
        # Initialize authentication attempts in session if not already set
        if not session.get('authentication_attempts'):
            session['authentication_attempts'] = 0
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            # Verify the user's credentials
            if not user or not user.verify_password(form.password.data) or not user.verify_pin(form.pin.data):
                session['authentication_attempts'] += 1
                # Check if the number of authentication attempts exceeded limit
                if session.get('authentication_attempts') >= 3:
                    flash(Markup('Number of login attempts exceeded. Please click <a href="/reset">here</a> to reset.'))
                    return render_template('users/login.html', form=form)
                attempts_remaining = 3 - session.get('authentication_attempts')
                flash("Please check your details and try again, {} login attempts remaining".format(attempts_remaining))
                return render_template('users/login.html', form=form)
            else:
                login_user(user)
                current_user.last_login = datetime.now()
                database.session.commit()

                if current_user.role == 'user':
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('admin.admin'))
    else:
        flash("You are already logged in.")
        return render_template("main/index.html")

    return render_template('users/login.html', form=form)


@users_blueprint.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # Render the account.html template with the current user's information
    return render_template('users/account.html',
                           acc_no=f"{current_user.id}",
                           email=f"{current_user.email}",
                           firstname=f"{current_user.firstname}",
                           lastname=f"{current_user.lastname}",
                           role=f"{current_user.role}")


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('main/index.html')


@users_blueprint.route('/reset')
def reset():
    if current_user.is_anonymous:
        session['authentication_attempts'] = 0
        return redirect(url_for('users.login'))
    else:
        flash("You do not have access to this page")
        return redirect(url_for('users.login'))


@users_blueprint.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = PasswordForm()

    if form.validate_on_submit():
        # Verify the current password
        if not current_user.verify_password(form.current_password.data):
            flash("Incorrect password. Try again.")
            return redirect(url_for('users.update_password'))

        # Ensure the new password is different from the current password
        if form.new_password.data == form.current_password.data:
            flash("New password must be different from current password. Try again.")
            return redirect(url_for('users.update_password'))

        # Update the user's password
        current_user.password = bcrypt.hashpw(form.new_password.data.encode('utf-8'), bcrypt.gensalt())
        database.session.commit()

        flash("Password successfully changed!")
        return redirect(url_for("users.account"))

    return render_template('users/update_password.html', form=form)


@users_blueprint.route('/setup_2fa')
def setup_2fa():
    if current_user.is_anonymous:
        if 'email' not in session:
            return render_template('main/index.html')

        user = User.query.filter_by(email=session['email']).first()

        if not user:
            return redirect(url_for('index'))
        del session['email']

        return (render_template('users/setup_2fa.html', email=user.email, uri=user.get_2fa_uri()),
                200, {
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Expires': '0'
                })
    else:
        flash("You can't access this page")
        return render_template('main/index.html')

