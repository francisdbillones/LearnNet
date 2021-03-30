from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import secrets
import os
import boto3

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(256)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = 'signin'
loginManager.login_message = 'You need to sign in for that.'
loginManager.login_message_category = 'warning'

# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

# set session type
app.config['SESSION_TYPE'] = 'filesystem'

# set maximum file size that a user can upload
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

# set maximum number of files a kit can have
app.config['MAX_KIT_FILE_COUNT'] = 10

# set valid files to be uploaded
app.config['ALLOWED_EXTENSIONS'] = [
    'pdf'
]

# set path for pdf.js viewer
app.config['PDF_JS_PATH'] = '/'.join(['pdf.js', 'web', 'viewer.html'])

# aws S3 setup
app.config['AWS_S3_BUCKET_NAME'] = os.environ.get('AWS_S3_BUCKET_NAME')
app.config['AWS_ACCESS_KEY'] = os.environ.get('AWS_ACCESS_KEY')
app.config['AWS_SECRET_ACCESS_KEY'] = os.environ.get('AWS_SECRET_ACCESS_KEY')

s3 = boto3.resource(
    's3',
    aws_access_key_id=app.config['AWS_ACCESS_KEY'],
    aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
)

session = Session(app)

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response


@app.context_processor
def inject_s3():
    return dict(s3=s3)


@app.context_processor
def inject_app():
    return dict(app=app)


@app.context_processor
def inject_bad_search_image_url():
    url = s3.meta.client.generate_presigned_url('get_object', Params={
        'Bucket': app.config['AWS_S3_BUCKET_NAME'],
        'Key': '/'.join(['images', 'barren-wasteland.jpg']),
        'ResponseContentType': 'image/jpeg'
    })

    return dict(bad_search_image_url=url)


from learn_net import routes