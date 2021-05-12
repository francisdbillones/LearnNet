from learn_net import app, s3
from werkzeug.utils import secure_filename
from PIL import Image
from flask_login import current_user
from flask import request, redirect

import secrets
import os
import functools
import io


def save_profile_picture(picture_file):
    if current_user.pfp_file == 'default.jpg':
        hexed_filename = secrets.token_hex(13)
        extension = os.path.splitext(picture_file.filename)[1]

        new_filename = hexed_filename + extension
        current_user.pfp_file = new_filename

        object_key = '/'.join(['images', 'profile_pictures', new_filename])
    else:
        object_key = '/'.join(['images', 'profile_pictures',
                               current_user.pfp_file])

    resized_image = Image.open(picture_file).resize((125, 125))

    with io.BytesIO() as final_picture:
        extension = os.path.splitext(picture_file.filename)[1][1::]
        resized_image.save(final_picture, format=extension)
        final_picture.seek(0)

        s3.Bucket(app.config['AWS_S3_BUCKET_NAME']).\
            upload_fileobj(final_picture, object_key, ExtraArgs={
                'ContentType': picture_file.mimetype
            })


def save_kit_file(kitID, file):
    filename = secure_filename(file.filename)
    object_key = '/'.join(['user_kits', str(kitID), filename])

    s3.Bucket(app.config['AWS_S3_BUCKET_NAME']).\
        upload_fileobj(file, object_key, ExtraArgs={
            'ContentType': file.mimetype
        })

    return filename


def rename_kit_file(kitID, old_filename, new_filename):
    new_filename = secure_filename(new_filename)

    # if new filename has no extension, assume the extension from the
    # previous filename
    if not os.path.splitext(new_filename)[1]:
        old_ext = os.path.splitext(old_filename)[1]
        new_filename = ''.join([new_filename, old_ext])

    old_object_key = '/'.join(['user_kits', str(kitID), old_filename])
    new_object_key = '/'.join(['user_kits', str(kitID), new_filename])

    # copy object from old path to new path
    copy_source = {
        'Bucket': app.config['AWS_S3_BUCKET_NAME'],
        'Key': old_object_key
    }
    s3.Bucket(app.config['AWS_S3_BUCKET_NAME']).copy(
        copy_source, new_object_key)

    # delete the old object
    s3.Object(app.config['AWS_S3_BUCKET_NAME'], old_object_key).delete()

    return new_filename


def delete_kit_file(kitID, file):
    filename = secure_filename(file.filename)
    object_key = '/'.join(['user_kits', str(kitID), filename])

    # remove the object
    s3.Object(app.config['AWS_S3_BUCKET_NAME'], object_key).delete()


def allowed_file(filename):
    extension = os.path.splitext(filename)[1][1::]

    return extension in app.config['ALLOWED_EXTENSIONS']


def sslify(route):
    @functools.wraps(route)
    def wrapper_sslify(*args, **kwargs):
        if os.environ.get('DEV'):
            return route(*args, **kwargs)
        protocol, url = request.url.split('://')
        if protocol == 'http':
            return redirect(f'https://{url}')
        return route(*args, **kwargs)
    return wrapper_sslify
