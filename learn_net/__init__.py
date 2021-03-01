from flask import Flask, session, url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import secrets
import os

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
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024; # 50 MB

# set maximum number of files a kit can have
app.config['MAX_KIT_FILE_COUNT'] = 10

# set valid files to be uploaded
app.config['ALLOWED_EXTENSIONS'] = [
    'pdf'
]

Session(app)

# create images folder
images_path = os.path.join(app.root_path, 'static', 'images')
if not os.path.exists(images_path):
    os.makedirs(images_path)
    # create profile_pictures folder
    profile_pictures_path = os.path.join(app.root_path, images_path, 'profile_picutres')
    if not os.path.isdir(profile_pictures_path):
        os.makedirs(profile_pictures_path)

# create user_kits folder
user_kits_path = os.path.join(app.root_path, 'static', 'user_kits')
if not os.path.exists(user_kits_path):
    os.makedirs(user_kits_path)

# download pdf.js dependency


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response

from learn_net import routes