from open_ed_web import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    pfp_file = db.Column(db.String(30), nullable=False, default='default.jpg') # NOT AN ACTUAL IMAGE. just the image file name
    school = db.Column(db.String(30), nullable=True)
    uploads = db.relationship('Content', backref='uploader', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.pfp_file}')"

# content that users can see, upload, and use
class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_uploaded = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.now())
    title = db.Column(db.String(30), unique=False, nullable=False, default=date_uploaded)
    school = db.Column(db.String(30), unique=False, nullable=True)   
    content_file = db.Column(db.String(20), unique=False, nullable=False)
    
    def __repr__(self):
        return f"Content('{self.title}', '{self.date_uploaded}')"
    
    
    
