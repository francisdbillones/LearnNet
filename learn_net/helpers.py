from learn_net import s3
from learn_net.models import Kit
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
        
        local_path = os.path.join(app.root_path, 'static', 'images', 'profile_pictures', new_filename)
    else:
        local_path = os.path.join(app.root_path, 'static', 'images', 'profile_pictures', current_user.pfp_file)
    
    image = Image.open(picture_file)
    image.thumbnail((125, 125))
    image.save(local_path)

def delete_profile_picture(picture_file):
    path = os.path.join(app.root_path, 'static', 'images', 'profile_pictures', picture_file.filename)
    os.remove(path)

# create a kit folder if it doesn't exist, else, just return the path
def create_kit_folder(kitID):
    path = os.path.join(app.root_path, 'static', 'user_kits', str(kitID))
    
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def delete_kit_folder(kitID):
    path = os.path.join(app.root_path, 'static', 'user_kits', str(kitID))
    if os.path.exists(path):
        os.rmdir(path)

def save_kit_file(kitID, file):
    filename = secure_filename(file.filename)
    folder_path = create_kit_folder(kitID)
    file_path = os.path.join(folder_path, filename)
    
    file.save(file_path)
    
    return filename

def rename_kit_file(kitID, old_filename, new_filename):
    new_filename = secure_filename(new_filename)
    
    # if new filename has no extension, assume the extension from the previous filename
    if not os.path.splitext(new_filename)[1]:
        old_ext = os.path.splitext(old_filename)[1]
        new_filename = ''.join([new_filename, old_ext])
    
    kit_path = os.path.join(app.root_path, 'static', 'user_kits', str(kitID))
    
    old_path = os.path.join(kit_path, old_filename)
    new_path = os.path.join(kit_path, new_filename)
    
    os.rename(old_path, new_path)
    
    return new_filename

def delete_kit_file(kitID, file):
    filename = secure_filename(file.filename)
    path = os.path.join(app.root_path, 'static', 'user_kits', str(kitID), filename)
    
    os.remove(path)
    
def allowed_file(filename):
    extension = os.path.splitext(filename)[1][1::]
    
    return extension in app.config['ALLOWED_EXTENSIONS']