from flask import Flask, render_template, redirect, request, session, url_for
from flask_session import Session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from helpers import *

import secrets

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(256)

# # flask-login login manager
# loginManager = LoginManager()
# loginManager.init_app(app)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        flash('Account created!', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)
    
@app.route("/signin", methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('signin.html', form=form)

@app.route('/browse', methods=['GET', 'POST'])
def browse():
    pass

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    pass

if __name__ == '__main__':
    app.run(debug=True)

        