from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import app
from .extensions import db
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    profile = db.relationship('Profile', backref='user', uselist=False)
    posts = db.relationship('ForumPost', backref='author', lazy='dynamic')
    events = db.relationship('Event', backref='organizer', lazy='dynamic')
    is_tutor = db.Column(db.Boolean, default=False)  # Indicates if the user is available for tutoring
    sessions = db.relationship('TutoringSession', foreign_keys='TutoringSession.tutor_id', backref='tutor', lazy='dynamic')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __init__(self, username, email):
        self.username = username
        self.email = email

class Profile(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    bio = db.Column(db.Text)
    major = db.Column(db.String(100))
    interests = db.Column(db.String(200))
    year_of_study = db.Column(db.Integer)

class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('forum_post.id'))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.Text)
    date = db.Column(db.DateTime)
    location = db.Column(db.String(120))
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class TutoringSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100))
    session_time = db.Column(db.DateTime)
    location = db.Column(db.String(120))
    tutor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('tutoring_session.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(50))
