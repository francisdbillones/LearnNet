from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from learn_net.models import User

# registration form
class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=30)])
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

# log in form
class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=100)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')
    
    # check if the user exists
    def validate_email(self, email):
        if not User.query.filter_by(email=email.data).first():
            raise ValidationError('That user does not exist. Are you trying to make an account?')
        
# form to allow user to edit their profile information ex. change username or add a profile picture
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    pfp_file = FileField('Profile picture', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField('Update info')
    
    # check that the username isn't the same as the current username and the chosen username isn't taken
    def validate_username(self, username):
        if current_user.username != username.data:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError('That username is taken. Please choose a different one.')  

# form for users to upload new content (documents, slides, etc)
class UploadContentForm(FlaskForm):
    title = StringField('Title', description='Add a title.', validators=[DataRequired(), Length(min=5, max=30)])
    file = FileField('File', validators=[FileAllowed([
        'doc', 'docx', 'pdf', 'odt', # document formats
        'ppt', 'pptx', 'pptm' # slideshow formats
    ])])
    school = StringField('School', description="From what school is this from? If you don't set anything, it'll be your school by default.")
    category = SelectField('Category', description='For what topic is this for?', choices=[
        'Language', 'Mathematics', 'Science', 'Health', 'Physical Education', 'Art', 'Music', 'Other'
    ])
    tags = StringField('Tags', description='Tags provide unique identification. Add some so that others can search for your uploads easier. Seperate tags with a comma.')
    submit = SubmitField('Post')