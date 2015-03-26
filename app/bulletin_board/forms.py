from flask_wtf import Form
from wtforms import BooleanField, HiddenField, PasswordField, \
    TextField, TextAreaField, validators


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField(
        'Email Address',
        [validators.Email(), validators.Length(min=6, max=255)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])


class LoginForm(Form):
    email = TextField(
        'Email Address',
        validators=[validators.Required(), validators.Email()])
    password = PasswordField('Password', validators=[validators.Required()])


class AddPostForm(Form):
    title = TextField('Title', validators=[validators.Required()])
    message = TextAreaField('Message', validators=[validators.Required()])
    id = HiddenField()
