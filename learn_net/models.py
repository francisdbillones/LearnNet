from learn_net import db, loginManager

from datetime import datetime
from flask_login import UserMixin


@loginManager.user_loader
def load_user(userID):
    return User.query.get(int(userID))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    pfp_file = db.Column(db.String(30), nullable=False, default='default.jpg') # NOT AN ACTUAL IMAGE. just the image file name
    school = db.Column(db.String(30), nullable=True)
    uploads = db.relationship('Content', backref='author', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.pfp_file}')"

class ContentTag(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    tag = db.Column(db.String(20))

# content that users can see, upload, and use
class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_uploaded = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.now())
    title = db.Column(db.String(30), unique=False, nullable=False)
    school = db.Column(db.String(30), unique=False, nullable=True)   
    content_file = db.Column(db.String(20), unique=False, nullable=False)
    file_type = db.Column(db.String(20), unique=False, nullable=False)
    tags = db.relationship('ContentTag', backref='content_tagged', lazy=True)
    
    def __repr__(self):
        return f"Content('{self.title}', '{self.date_uploaded}')"
    
    
    
