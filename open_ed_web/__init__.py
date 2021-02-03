from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

import secrets

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(256)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

# set session type
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response

from open_ed_web import routes