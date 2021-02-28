import secrets

from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, RadioField, FileField, MultipleFileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed

from flask_login import current_user

from learn_net.models import User, Kit, KitTag
from learn_net.helpers import allowed_file

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
    
    # check that the username isn't taken
    def validate_username(self, username):
        if current_user.username != username.data:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError('That username is taken. Please choose a different one.')  

class CreateKitForm(FlaskForm):
    title = StringField('Title', description='Add a title.', validators=[DataRequired(), Length(min=5, max=30)])
    
    kit_description = TextAreaField('Description', description='Describe this kit.', validators=[DataRequired(), Length(min=20)])
    
    category = SelectField('Category', description='For what topic is this for?', choices=[
        'Language', 'Mathematics', 'Science', 'Health', 'Physical Education', 'Art', 'Music', 'Other'
    ])
    
    tags = StringField('Tags', description='Add a few tags. Separate tags with commas.', validators=[DataRequired(), Length(min=3, max=50)]) 
    
    submit = SubmitField('Create kit')
    
    def validate_tags(self, tags):
        for tag in tags.data.split(','):
            if len(tag) > 20:
                raise ValidationError('That tag is too long.')

def EditKitForm(kit):
    class form(FlaskForm):
        title = StringField('Title', description='Edit your title.', validators=[Length(min=5, max=30)])
        
        kit_description = TextAreaField('Description', description='Describe this kit.', validators=[Length(min=20)])
        
        category = SelectField('Category', description='For what topic is this for?', choices=[
            'Language', 'Mathematics', 'Science', 'Health', 'Physical Education', 'Art', 'Music', 'Other'
        ])
        
        tags = StringField('Tags', description='Add a few tags. Separate tags with commas.', validators=[Length(min=3, max=50)])
        
        submit = SubmitField('Save changes')
    
        def validate_tags(self, tags):
            for tag in tags.data.split(','):
                if len(tag) > 20:
                    raise ValidationError('Some of your tags are too long. Tags have a 20 character limit. Make sure to separate tags with commas.')
    
    for file in kit.files:
        setattr(form, f'{file.filename}-filename', StringField('Filename', validators=[DataRequired(), Length(min=5, max=30)]))
    
    editKitForm = form()
    
    return editKitForm

# form for users to upload new files to kit (documents, etc.)
class UploadKitFilesForm(FlaskForm):
    files = MultipleFileField('Add more files', validators=[DataRequired()], description='You can upload up to 50 MB.')
    submit = SubmitField('Upload')
    
    def validate_files(self, files):
        for file in files.data:
            if not allowed_file(file.filename):
                raise ValidationError('That file type is not supported')
            if len(file.filename) > 30:
                raise ValidationError(f'The length of one of your file\'s names, particularly "{file.filename}", is too long.')

# simple form with text search only
class SimpleSearchForm(FlaskForm):
    query = StringField('Search query', validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField('Search')

# form for users to search + filter
class ExtendedSearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired(), Length(min=5, max=100)])
    sort_by = RadioField('Sort by', choices=[
        'Relevancy', 'Recency'
    ])
    school = StringField('School', validators=[Length(min=2, max=50)])
    submit = SubmitField('Search')