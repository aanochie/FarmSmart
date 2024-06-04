from flask import Blueprint, render_template

from app import requires_roles, login_required
from dbSetup import User
# Written by: Malak (c2001143)
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin')
# Ensure the user is logged in before accessing the admin page
@login_required
# Ensure the user has the 'admin' role before accessing the admin page
@requires_roles('admin')
def admin():
    # Render the admin page template when accessing the /admin route
    return render_template('admin/admin.html')


@admin_blueprint.route('/view_all_users')
@login_required
@requires_roles('admin')
def view_all_users():
    # Query the User table to get all users with the role 'user'
    current_users = User.query.filter_by(role='user').all()
    # Render the admin.html template and pass the current_users to the template
    return render_template('admin/admin.html', current_users=current_users)
