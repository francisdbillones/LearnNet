from werkzeug.utils import secure_filename
from learn_net import app
from PIL import Image
from flask_login import current_user
import secrets
import os

def save_profile_picture(picture_file):
    if current_user.pfp_file == 'default.jpg':
        hexed_filename = secrets.token_hex(13)
        extension = os.path.splitext(picture_file.filename)[1]
        
        new_filename = hexed_filename + extension
        current_user.pfp_file = new_filename
        
        path = os.path.join(app.root_path, 'static', 'images', 'profile_pictures', new_filename)
    else:
        path = os.path.join(app.root_path, 'static', 'images', 'profile_pictures', current_user.pfp_file)
    
    image = Image.open(picture_file)
    image.thumbnail((125, 125))
    image.save(path)

def delete_profile_picture(picture_file):
    path = os.path.join(app.root_path, 'static', 'images', 'profile_pictures', picture_file.filename)
    os.remove(path)

def create_kit_folder(kitID):
    path = os.path.join(app.root_path, 'static', 'user_kits', str(kitID))
    
    if not os.path.exists(path):
        os.makedirs(path)

def delete_kit_folder(kitID):
    path = os.path.join(app.root_path, 'static', 'user_kits', str(kitID))
    if os.path.exists(path):
        os.rmdir(path)

def save_kit_file(kitID, file):
    filename = secure_filename(file.filename)
    path = os.path.join(app.root_path, 'static', 'user_kits', str(kitID), filename)
    
    file.save(path)
    
    return filename

def delete_kit_file(kitID, file):
    filename = secure_filename(file.filename)
    path = os.path.join(app.root_path, 'static', 'user_kits', str(kitID), filename)
    
    os.remove(path)
    
def allowed_file(filename):
    extension = os.path.splitext(filename)[1][1::]
    
    return extension in app.config['ALLOWED_EXTENSIONS']

    
