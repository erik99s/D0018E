from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    firstName = StringField('firstName', [DataRequired()])
    lastName = StringField('lastName', [DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    confirm_email = StringField('confirm email', validators=[DataRequired(), EqualTo('email')])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
      
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    firstName = StringField('firstName', [DataRequired()])
    lastName = StringField('lastName', [DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember me')
    submit = SubmitField('sign in')