from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    firstName = StringField('firstName', [DataRequired()])
    lastName = StringField('lastName', [DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Passwrod', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
      
    submit = SubmitField('sign in')

class LoginForm(FlaskForm):
    firstName = StringField('firstName', [DataRequired()])
    lastName = StringField('lastName', [DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('passwrod', validators=[DataRequired()])
    remember = BooleanField('remember me')
    submit = SubmitField('login in')