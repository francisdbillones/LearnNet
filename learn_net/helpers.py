from learn_net import app
from PIL import Image
import secrets
import os

def delete_profile_picture(picture_file):
    picture_path = os.path.join(app.root_path, 'static', 'images', 'profile_pictures', picture_file)
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

def save_content_file(content_file):
    hexed_filename = secrets.token_hex(16)
    extension = os.path.splitext(content_file.filename)[1]
    content_filename = hexed_filename + extension
    content_path = os.path.join(app.root_path, 'static', 'user_uploads', content_filename)
    
    content_file.save(content_path)
    
    return content_filename

FILE_TYPES = {
    '.doc': 'Document',
    '.docx': 'Document',
    '.pdf': 'Document',
    '.odt': 'Document',
    
    '.ppt': 'Slideshow',
    '.pptx': 'Slideshow',
    '.pptm': 'Slideshow'
}

def getFileType(file):
    extension = os.path.splitext(file.filename)[1]
    return FILE_TYPES[extension]
    
