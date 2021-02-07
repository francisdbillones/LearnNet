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
    uploads = db.relationship('Article', backref='author', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.pfp_file}')"

class ArticleTag(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    tag = db.Column(db.String(20))

# articles that users can see, upload, download, and just use in general
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_uploaded = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.now())
    title = db.Column(db.String(30), unique=False, nullable=False)
    article_description = db.Column(db.Text, unique=False, nullable=False)
    school = db.Column(db.String(30), unique=False, nullable=True)   
    file = db.Column(db.String(20), unique=False, nullable=False)
    file_type = db.Column(db.String(20), unique=False, nullable=False)
    tags = db.relationship('ArticleTag', backref='article_tagged', lazy=True)
    
    def __repr__(self):
        return f"Article('{self.title}', '{self.date_uploaded}')"
    
    
    
