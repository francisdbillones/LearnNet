from flask import render_template, redirect, url_for, flash, request
from open_ed_web.forms import *
from open_ed_web.models import User, Content
from open_ed_web import app, db, bcrypt, session
from flask_login import login_user, logout_user, login_required


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # create a new user and sign in
    
    form = SignUpForm()
    if form.validate_on_submit():
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        )

        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Account created!', 'success')
        
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)
    
@app.route("/signin", methods=['GET', 'POST'])
def signin():
    # sign in user
    
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            
            next_page = request.args.get('next')
            flash('Successfully signed in!', 'success')
            return redirect(url_for('index')) if not next_page else redirect(next_page)
        else:
            flash('Error signing in. Check your password.', 'danger')
    return render_template('signin.html', form=form)

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
    return render_template('account.html')

@app.route('/browse', methods=['GET', 'POST'])
def browse():
    # browse index
    
    flash('That page does not exist yet, sorry.', 'info')
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    # upload new content
    
    flash('That page does not exist yet, sorry.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)