from flask import Flask, flash, redirect, render_template, request, session, url_for
from functools import wraps
from flask_login import current_user
from open_ed_web import app
from PIL import Image
import secrets
import os

def delete_profile_picture(picture_file):
    picture_path = os.path.join(app.root_path, 'static', 'images', 'profile_pictures', picture_filename)
    os.remove(picture_path)

def save_profile_picture(picture_file):
    hexed_filename = secrets.token_hex(16)
    extension = os.path.splitext(picture_file.filename)[1]
    picture_filename = hexed_filename + extension
    picture_path = os.path.join(app.root_path, 'static', 'images', 'profile_pictures', picture_filename)
    
    image = Image.open(picture_file)
    image.thumbnail((125, 125))
    image.save(picture_path)
    
    return picture_filename
