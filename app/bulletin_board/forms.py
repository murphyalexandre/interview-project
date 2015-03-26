from flask_wtf import Form
from wtforms import BooleanField, TextField, PasswordField, validators


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Email(), validators.Length(min=6, max=255)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])


class LoginForm(Form):
    email = TextField(
        'email', validators=[validators.Required(), validators.Email()])
    password = PasswordField('password', validators=[validators.Required()])
