from learn_net import app
from PIL import Image
from flask_login import current_user
import secrets
import os

def save_profile_picture(picture_file):
    if current_user.pfp_file == 'default.jpg':
        hexed_filename = secrets.token_hex(16)
        extension = os.path.splitext(picture_file.filename)[1]
        
        new_filename = hexed_filename + extension
        current_user.pfp_file = new_filename
        
        path = os.path.join(app.root_path, 'static', 'images', 'profile_pictures', new_filename)
    else:
        path = os.path.join(app.root_path, 'static', 'images', 'profile_pictures', current_user.pfp_file)
    
    image = Image.open(picture_file)
    image.thumbnail((125, 125))
    image.save(path)

def save_article_file(file):
    hexed_filename = secrets.token_hex(16)
    extension = os.path.splitext(file.filename)[1]
    filename = hexed_filename + extension
    path = os.path.join(app.root_path, 'static', 'user_uploads', filename)
    
    file.save(path)
    
    return filename

FILE_CATEGORIES = [
    'Document',
    'Slideshow'
]

FILE_TYPES = {
    '.doc': FILE_CATEGORIES[0],
    '.docx': FILE_CATEGORIES[0],
    '.pdf': FILE_CATEGORIES[0],
    '.odt': FILE_CATEGORIES[0],
    
    '.ppt': FILE_CATEGORIES[1],
    '.pptx': FILE_CATEGORIES[1],
    '.pptm': FILE_CATEGORIES[1]
}

def getFileType(file):
    extension = os.path.splitext(file.filename)[1]
    return FILE_TYPES[extension]
    
