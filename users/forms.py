import re
from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields.simple import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, InputRequired


def character_check(form, field):
    excluded_chars = "*?!'^+%&/()=}][{$#@<>"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed")


def password_includes(form, password):
    p = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W|_)')
    if not p.match(password.data):
        raise ValidationError(
            "Password must contain 1 digit, 1 lowercase letter, 1 uppercase letter, and 1 special character")


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[Email(message='Please enter a valid email.'),
                                             InputRequired()])
    firstname = StringField('First Name', validators=[InputRequired(), character_check])
    lastname = StringField('Last Name', validators=[InputRequired(), character_check])
    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(min=6, max=15,
                                                            message='Password must be between 6 and 15 characters'),
                                                     password_includes])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[InputRequired(), EqualTo('password', message='Password must match')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Please input a valid email")])
    password = PasswordField(validators=[InputRequired()])
    pin = StringField(validators=[InputRequired(), Length(min=6, max=6, message="Your pin must be a 6 digit number.")])
    recaptcha = RecaptchaField()
    submit = SubmitField('Log In')


class PasswordForm(FlaskForm):
    current_password = PasswordField(id='password', validators=[InputRequired()])
    show_password = BooleanField('Show password', id='check')
    new_password = PasswordField(validators=[InputRequired(), Length(min=6, max=15,
                                                                    message='Password must be between 6 and 15 characters'),
                                             password_includes])
    confirm_new_password = PasswordField(
        validators=[InputRequired(), EqualTo('new_password', message='Password must match')])
    submit = SubmitField('Change Password')
