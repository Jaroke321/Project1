from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
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
    username = StringField('Username',
        validators=([Length(min=2, max=20)]))
    picture = FileField('Update Profile Picture',
        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

class ReviewForm(FlaskForm):
    rating =  DecimalField('Book Rating Out Of 10',
        validators=([DataRequired(), NumberRange(min=0, max=10)]))
    review = TextAreaField('Written Review')
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')
