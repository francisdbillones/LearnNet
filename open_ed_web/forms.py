from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from open_ed_web.models import User
from open_ed_web import bcrypt

# registration and sign in forms
class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=100)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign up')
    
    # check if username is not taken
    def validate_username(self, username):
        # if username exists, raise validation error
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('That username is taken. Are you trying to log in?')
    
    # check if email is not taken
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('That email is taken. Are you trying to log in?')

class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=100)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')
    
    # check if the user exists
    def validate_email(self, email):
        if not User.query.filter_by(email=email.data).first():
            raise ValidationError('That user does not exist. Are you trying to make an account?')
    