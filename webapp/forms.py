from wtforms import *

class UserRegistrationForm(Form):
    name = TextField('Name Surname', [validators.Required(), validators.Length(min=3, max=128, message="Your name should be minimum 3, maximum 128 characters.")])
    email = TextField('E-Mail', [validators.Required(), validators.Email(message='Wrong E-Mail address.')])
    team = TextField('RoboCup Team Name')
    country = TextField('Country')
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm',message='Password missmatch')])
    confirm = PasswordField('Repeat Password',[validators.Required()])


class LoginForm(Form):
    email = TextField('E-Mail', [validators.Required(), validators.Email(message='Invalid E-Mail address.')])
    password = PasswordField('Password', [validators.Required()])
