from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_fileName = db.Column(db.String(100))
    fileName = db.Column(db.String(100))
    bucket = db.Column(db.String(100))
    region = db.Column(db.String(100))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(150), unique=True)
    firstName = db.Column(db.String(150))
    password = db.Column(db.String(150))
    notes = db.relationship('Note')
    # posts = db.relationship('Post', backref='author', lazy=True)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    name = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    email = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    content = db.Column(db.Text)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    email = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    content = db.Column(db.Text)
