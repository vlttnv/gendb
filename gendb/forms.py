"""Form definitions."""

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class RegisterForm(Form):
    email = StringField('email', id='email', validators=[DataRequired()])
    pw1 = PasswordField('pw1', id='pw1', validators=[DataRequired()])
    pw2 = PasswordField('pw2', id='pw2', validators=[DataRequired()])


class LoginForm(Form):
    email = StringField('email', id='email', validators=[DataRequired()])
    pw1 = PasswordField('pw1', id='pw1', validators=[DataRequired()])
