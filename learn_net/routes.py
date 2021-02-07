from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from learn_net.forms import *
from learn_net.models import  User, Article, ArticleTag
from learn_net import app, db, bcrypt, session

from learn_net.helpers import save_profile_picture, save_article_file, getFileType

import secrets


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # create a new user and sign in
    
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

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
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
        return redirect(url_for('account'))
    
    elif request.method == 'GET':
        # pre-fill fields
        updateAccountForm.username.data = current_user.username
        updateAccountForm.email.data = current_user.email
    
    userArticles = Article.query.filter_by(user_id=current_user.id)
    
    profile_image = url_for('static', filename=f'images/{ current_user.pfp_file }')
    return render_template('account.html', profile_image=profile_image, updateAccountForm=updateAccountForm, userArticles=userArticles)

@app.route('/browse', methods=['GET', 'POST'])
def browse():
    # browse index
    # TODO browse route
    
    flash('That page does not exist yet, sorry.', 'info')
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    # upload new Article
    # TODO upload route
    
    uploadArticleForm = UploadArticleForm()
    
    if uploadArticleForm.validate_on_submit():
        article = Article(
            user_id = current_user.id,
            title = uploadArticleForm.title.data,
            article_description = uploadArticleForm.article_description.data,
            school = uploadArticleForm.school.data,
            file = save_article_file(uploadArticleForm.file.data),
            file_type = getFileType(uploadArticleForm.file.data)
        )
        db.session.add(article)
        db.session.flush()

        tags = [tag.strip() for tag in uploadArticleForm.tags.data.split()]
        for tag in tags:
            articleTag = ArticleTag(tag=tag, article_id=article.id)
            db.session.add(articleTag)
        
        db.session.commit()
        
        flash('Uploaded!', 'success')
        return redirect(url_for('account'))
    
    return render_template('upload.html', uploadArticleForm=uploadArticleForm)

@app.route('/article', methods=['GET', 'POST'])
def article():
    # TODO display articles
    return redirect('/')

@app.route('/getusername')
def getusername():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    result = user.username if user else None
    return jsonify({"username": result})

if __name__ == '__main__':
    app.run(debug=True)