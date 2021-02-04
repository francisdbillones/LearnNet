from flask import Flask, flash, redirect, render_template, request, session, url_for
from functools import wraps
from flask_login import current_user
from open_ed_web import app
import secrets
import os

def save_picture(picture_file):
    hexed_filename = secrets.token_hex(16)
    extension = os.path.splitext(picture_file.filename)[1]
    picture_filename = hexed_filename + extension
    picture_path = os.path.join(app.root_path, 'static/images/profile_pictures', picture_filename)
    picture_file.save(picture_path)
    
    return picture_filename