from flask import Flask, flash, redirect, render_template, request, session, url_for
from functools import wraps
from flask_login import current_user

# def login_required(f):
#     '''
#     Decorate routes to require login.

#     https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
#     '''
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not current_user.is_authenticated:
#             flash('You need to log in for that.', 'warning')
#             return redirect(url_for('signin'))
#         return f(*args, **kwargs)
#     return decorated_function