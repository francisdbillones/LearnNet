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
    # NOT AN ACTUAL IMAGE. just the image file name
    pfp_file = db.Column(db.String(30), nullable=False, default='default.jpg')
    school = db.Column(db.String(30), nullable=True)
    kits = db.relationship('Kit', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.pfp_file}')"


class Kit(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(30), unique=False, nullable=False)
    kit_description = db.Column(db.Text, unique=False, nullable=False)
    category = db.Column(db.String(20), unique=False, nullable=False)
    files = db.relationship('KitFile', backref='kit', lazy=True)
    youtube_video_ids = db.relationship(
        'YoutubeVideoId', backref='kit', lazy=True)
    tags = db.relationship('KitTag', backref='kit_tagged', lazy=True)

    def __repr__(self):
        return f"Kit(`{self.title}`, {self.kit_description}`)"


class KitTag(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    kit_id = db.Column(db.Integer, db.ForeignKey('kit.id'), nullable=False)
    tag = db.Column(db.String(20))


class KitFile(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    filename = db.Column(db.String(30), unique=False, nullable=False)
    date_uploaded = db.Column(
        db.DateTime, unique=False, nullable=False, default=datetime.now())
    kit_id = db.Column(db.Integer, db.ForeignKey('kit.id'), nullable=False)


class YoutubeVideoId(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    kit_id = db.Column(db.Integer, db.ForeignKey('kit.id'), nullable=False)
    video_id = db.Column(db.String(20), unique=False, nullable=False)
