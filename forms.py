from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField
from wtforms.widgets import TextArea
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
    submit = SubmitField('log in')

class AddToCartForm(FlaskForm):
    amount = IntegerField('productAmount', [DataRequired()])

class ratingForm(FlaskForm):
    rating = RadioField('star', choices=[('value','description'),('value_two','whatever')])
    title = StringField('title', [DataRequired()])
    comment = StringField('comment', widget=TextArea())