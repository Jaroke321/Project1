from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',
            validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password',
            validators=[DataRequired()])
    c_password = PasswordField('Confirm Password',
            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username',
            validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password',
            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    picture = FileField('Update Profile Picture',
        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
