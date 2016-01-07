"""Form definitions."""

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, HiddenField
from wtforms.validators import DataRequired


class RegisterForm(Form):
    email = StringField('email', id='email', validators=[DataRequired()])
    pw1 = PasswordField('pw1', id='pw1', validators=[DataRequired()])
    pw2 = PasswordField('pw2', id='pw2', validators=[DataRequired()])


class LoginForm(Form):
    email = StringField('email', id='email', validators=[DataRequired()])
    pw1 = PasswordField('pw1', id='pw1', validators=[DataRequired()])


class AddProjectForm(Form):
    name = StringField(
        'name',
        id='name',
        validators=[DataRequired()]
    )
    description = TextAreaField(
        'description',
        id='description',
        validators=[DataRequired()]
    )


class AddProjectContributorForm(Form):
    email = StringField(
        'name',
        id='name',
        validators=[DataRequired()]
    )
    project_id = HiddenField(
        'project_id',
        id='project_id',
        validators=[DataRequired()]
    )
