from flask import Flask, session
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

Session(app)

# create images folder
images_path = os.path.join(app.root_path, 'learn_net', 'static', 'images')
if not os.path.isdir(image_path):
    # create profile_pictures folder
    if not os.path.isdir

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response

from learn_net import routes