from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from learn_net.forms import *
from learn_net.models import  User, Kit, KitFile, KitTag
from learn_net import app, db, bcrypt, session

from learn_net.helpers import save_profile_picture, save_kit_file, get_file_type, create_kit_folder

from datetime import datetime

import secrets

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # create a new user, then sign them in
    
    signUpForm = SignUpForm()
    if signUpForm.validate_on_submit():
        
        user = User(
            username=signUpForm.username.data,
            email=signUpForm.email.data,
            password=bcrypt.generate_password_hash(signUpForm.password.data).decode('utf-8')
        )

        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Account created!', 'success')
        
        return redirect(url_for('index'))
    return render_template('signup.html', signUpForm=signUpForm)
    
@app.route("/signin", methods=['GET', 'POST'])
def signin():
    # sign in user
    
    signInForm = SignInForm()
    if signInForm.validate_on_submit():
        user = User.query.filter_by(email=signInForm.email.data).first()
        
        if bcrypt.check_password_hash(user.password, signInForm.password.data):
            login_user(user, remember=signInForm.remember.data)
            
            next_page = request.args.get('next')
            flash('Successfully signed in!', 'success')
            return redirect(url_for('index')) if not next_page else redirect(next_page)
        else:
            flash('Error signing in. Check your password.', 'danger')
    return render_template('signin.html', signInForm=signInForm)

@app.route('/signout')
@login_required
def signout():
    # sign out user
    
    session.clear()
    logout_user()
    flash('You are logged out.', 'danger')
    
    return redirect(url_for('index'))

@app.route('/<string:username>', methods=['GET', 'POST'])
def account(username):
    # view account information
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        flash('That page does not exist.', 'danger')
        return redirect(url_for('index'))
    
    updateAccountForm = UpdateAccountForm()

    if updateAccountForm.validate_on_submit():
        changed = False
        if current_user.username != updateAccountForm.username.data:
            current_user.username = updateAccountForm.username.data
            changed = True

        if current_user.email != updateAccountForm.email.data:
            current_user.email = updateAccountForm.email.data
            changed = True

        if updateAccountForm.pfp_file.data:
            save_profile_picture(updateAccountForm.pfp_file.data)
            changed = True

        db.session.commit()

        if changed:
            flash('Your account has been updated.', 'info')
            
            # do this to update the route
            return redirect(url_for('account', username=user.username))

    elif request.method == 'GET':
        # pre-fill fields
        updateAccountForm.username.data = current_user.username
        updateAccountForm.email.data = current_user.email
        
    profile_image = url_for('static', filename=f'images/{ current_user.pfp_file }')
    return render_template('account.html', profile_image=profile_image, updateAccountForm=updateAccountForm)

@app.route('/<string:username>/edit', methods=['GET', 'POST'])
@login_required
def edit_account(username):
    # allow user to edit their account information
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        flash('That user does not exist.', 'danger')
        return redirect(url_for('index'))
    elif user.username != current_user.username:
        flash('You are not allowed to do that.', 'danger')
        return redirect(url_for('index'))
    
    updateAccountForm = UpdateAccountForm()

    if updateAccountForm.validate_on_submit():
        changed = False
        if current_user.username != updateAccountForm.username.data:
            current_user.username = updateAccountForm.username.data
            changed = True

        if current_user.email != updateAccountForm.email.data:
            current_user.email = updateAccountForm.email.data
            changed = True

        if updateAccountForm.pfp_file.data:
            save_profile_picture(updateAccountForm.pfp_file.data)
            changed = True

        db.session.commit()

        if changed:
            flash('Your account has been updated.', 'info')

    elif request.method == 'GET':
        # pre-fill fields
        updateAccountForm.username.data = current_user.username
        updateAccountForm.email.data = current_user.email
        
    profile_image = url_for('static', filename=f'images/{ current_user.pfp_file }')
    return render_template('account.html', profile_image=profile_image, updateAccountForm=updateAccountForm)

@app.route('/browse', methods=['GET', 'POST'])
def browse():
    # browse index
    # TODO browse route
    
    extendedSearchForm = ExtendedSearchForm()
    
    return render_template('browse.html', extendedSearchForm=extendedSearchForm)

@app.route('/kits')
@login_required
def kits():
    # view user's kits, saved kits, favourited kits, etc.
    
    userKits = Kit.query.filter_by(user_id = current_user.id)
    
    return render_template('kits.html', userKits=userKits)

@app.route('/kits/create', methods=['GET', 'POST'])
@login_required
def create_kit():
    # allow users to create kit
    
    createKitForm = CreateKitForm()
    
    if createKitForm.validate_on_submit():
        kit = Kit(
            owner = current_user,
            title = createKitForm.title.data,
            kit_description = createKitForm.kit_description.data,
            category = createKitForm.category.data
        )
        db.session.add(kit)
        db.session.flush() # do this so that kit.id is generated without having to commit first
        
        for tag in createKitForm.tags.data.split(','):
            kitTag = KitTag(tag = tag, kit_id = kit.id)
            db.session.add(kitTag)
        
        db.session.commit()
        
        create_kit_folder(kit.id)
        
        flash('Successfully created kit!', 'success')
        return redirect(url_for('kits'))
        
    return render_template('create_kit.html', createKitForm=createKitForm)

@app.route('/kits/<int:kitID>', methods=['GET', 'POST'])
def view_kit(kitID):
    # view kit information
    
    kit = Kit.query.filter_by(id = kitID).first()
    
    if not kit:
        flash('That kit does not exist.', 'danger')
        return redirect(url_for('kits'))
    
    uploadKitFilesForm = UploadKitFilesForm()
    
    if uploadKitFilesForm.validate_on_submit():
        # check that the files the user uploaded doesn't exceed maximum number of files allowed
        total_file_count = len(kit.files) + len(uploadKitFilesForm.files.data)
        if total_file_count > app.config['MAX_KIT_FILE_COUNT']:
            flash('A kit can only have a maximum of 10 files.', 'warning')
            return redirect(url_for('kits'))
        
        for f in uploadKitFilesForm.files.data:
            file = KitFile(filename=save_kit_file(kit.id, f), file_type = get_file_type(f), kit_id = kit.id)
            db.session.add(file)
        db.session.commit()
        
        flash('Your changes have been saved.', 'success')
    
    return render_template('view_kit.html', kit=kit, uploadKitFilesForm=uploadKitFilesForm)    

@app.route('/kits/<int:kitID>/edit', methods=['GET', 'POST'])
@login_required
def edit_kit(kitID):
    kit = Kit.query.filter_by(id = kitID).first()
    if kit.owner.id != current_user.id:
        flash('You\'re not allowed to do that.', 'danger')
        return redirect(url_for('kits'))

    editKitForm = EditKitForm()
    if editKitForm.validate_on_submit():
        changed = False
        
        if editKitForm.title.data:
            kit.title = editKitForm.title.data
            changed = True
        
        if editKitForm.kit_description.data:
            kit.kit_description = editKitForm.kit_description.data
            changed = True
        
        if editKitForm.category.data:
            kit.category = editKitForm.category.data
            changed = True
        
        if editKitForm.tags.data:
            for tag in kit.tags:
                db.session.delete(tag)
            for tag in editKitForm.tags.data.split(','):
                new_tag = KitTag(tag = tag, kit_id = kit.id)
                db.session.add(new_tag)
                print(new_tag.tag)
            changed = True
        
        db.session.commit()
        
        if changed:
            flash('Changes saved.', 'success')
            return redirect(url_for('view_kit', kitID=kitID))
    
    elif request.method == 'GET':
        editKitForm.title.data = kit.title
        editKitForm.kit_description.data = kit.kit_description
        editKitForm.category.data = kit.category
        editKitForm.tags.data = ', '.join([tag.tag for tag in kit.tags])
    
    return render_template('edit_kit.html', editKitForm=editKitForm)

@app.route('/getusername')
def getusername():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    result = user.username if user else None
    return jsonify({"username": result})

if __name__ == '__main__':
    app.run(debug=True)