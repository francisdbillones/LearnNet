from flask import render_template, redirect, url_for
from open_ed_web.forms import *
from open_ed_web import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    # create a new user and sign in
    
    form = SignUpForm()
    if form.validate_on_submit():
        flash('Account created!', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)
    
@app.route("/signin", methods=['GET', 'POST'])
def signin():
    # sign in user
    
    form = SignInForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('signin.html', form=form)

@app.route('/browse', methods=['GET', 'POST'])
def browse():
    # browse index
    
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # upload new content
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)