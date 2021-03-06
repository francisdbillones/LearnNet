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
        
        object_key = os.path.join('images', 'profile_pictures', new_filename)
    else:
        object_key = os.path.join('images', 'profile_pictures', current_user.pfp_file)
    
    local_path = os.path.join(app.root_path, 'static', object_key)
    
    image = Image.open(picture_file)
    image.thumbnail((125, 125))
    image.save(local_path)

    s3.Bucket(app.config['AWS_S3_BUCKET_NAME']).upload_file(local_path, object_key)

def save_kit_file(kitID, file):
    filename = secure_filename(file.filename)
    object_key = os.path.join('user_kits', str(kitID), filename)
    local_path = os.path.join(app.root_path, 'static', object_key)
    
    # save file to local, temporarily
    file.save(local_path)
    
    # upload file with content type set to application/pdf. for some reason, when we don't do this, content type gets set to binary/octet-stream, and the browser can't view the pdf file.
    s3.Bucket(app.config['AWS_S3_BUCKET_NAME']).upload_file(local_path, object_key, ExtraArgs={
        'ContentType': 'application/pdf'
    })
    
    # now delete the local file
    os.remove(local_path)
    
    return filename

def rename_kit_file(kitID, old_filename, new_filename):
    new_filename = secure_filename(new_filename)
    
    # if new filename has no extension, assume the extension from the previous filename
    if not os.path.splitext(new_filename)[1]:
        old_ext = os.path.splitext(old_filename)[1]
        new_filename = ''.join([new_filename, old_ext])

    old_object_key = os.path.join('user_kits', str(kitID), old_filename)    
    new_object_key = os.path.join('user_kits', str(kitID), new_filename)
    
    # copy object from old path to new path
    copy_source = {
        'Bucket': app.config['AWS_S3_BUCKET_NAME'],
        'Key': old_object_key
    }
    s3.Bucket(app.config['AWS_S3_BUCKET_NAME']).copy(copy_source, new_object_key)
    
    # delete the old object
    s3.Object(app.config['AWS_S3_BUCKET_NAME'], old_object_key).delete()
    
    return new_filename

def delete_kit_file(kitID, file):
    filename = secure_filename(file.filename)
    object_key = os.path.join(app.root_path, 'static', 'user_kits', str(kitID), filename)
    
    # remove the object
    s3.Object(app.config['AWS_S3_BUCKET_NAME'], object_key).delete()
    
def allowed_file(filename):
    extension = os.path.splitext(filename)[1][1::]
    
    return extension in app.config['ALLOWED_EXTENSIONS']