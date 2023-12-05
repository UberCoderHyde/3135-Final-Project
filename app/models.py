from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db

# Association table for the many-to-many relationship between tutors and courses
tutors_courses = db.Table('tutors_courses',
    db.Column('tutor_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

# Association table for the many-to-many relationship between courses and forums
courses_forums = db.Table('courses_forums',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('forum_id', db.Integer, db.ForeignKey('forum.id'), primary_key=True)
)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    description = db.Column(db.Text, default='')
    profile = db.relationship('Profile', back_populates='user', uselist=False)
    events = db.relationship('Event', back_populates='organizer', lazy='dynamic')
    posts = db.relationship('ForumPost', back_populates='author', lazy='dynamic')
    comments = db.relationship('Comment', back_populates='commenter', lazy='dynamic')
    is_tutor = db.Column(db.Boolean, default=False)  # Indicates if the user is available for tutoring
    sessions = db.relationship('TutoringSession', back_populates='tutor', lazy='dynamic')
    courses = db.relationship('Course', secondary=tutors_courses, back_populates='tutors')
    forums = db.relationship('Forum', back_populates='user', lazy='dynamic')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Profile(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    bio = db.Column(db.Text)
    major = db.Column(db.String(100))
    interests = db.Column(db.String(200))
    year_of_study = db.Column(db.Integer)
    user = db.relationship('User', back_populates='profile')

class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='posts')
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'))
    forum = db.relationship('Forum', back_populates='posts')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    commenter = db.relationship('User', back_populates='comments')
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'))
    forum = db.relationship('Forum', back_populates='comments')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.Text)
    date = db.Column(db.DateTime)
    location = db.Column(db.String(120))
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    organizer = db.relationship('User', back_populates='events')

class TutoringSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100))
    session_time = db.Column(db.DateTime)
    location = db.Column(db.String(120))
    tutor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    enrollments = db.relationship('Enrollment', back_populates='session', lazy='dynamic')
    tutor = db.relationship('User', back_populates='sessions')
    course = db.relationship('Course', back_populates='sessions')

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('tutoring_session.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(50))
    session = db.relationship('TutoringSession', back_populates='enrollments')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sessions = db.relationship('TutoringSession', back_populates='course', lazy='dynamic')
    tutors = db.relationship('User', secondary=tutors_courses, back_populates='courses')
    forums = db.relationship('Forum', secondary=courses_forums, back_populates='courses')

class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Add this line
    user = db.relationship('User', back_populates='forums')  # Assuming you have a User model

    posts = db.relationship('ForumPost', back_populates='forum', lazy='dynamic')
    comments = db.relationship('Comment', back_populates='forum', lazy='dynamic')
    courses = db.relationship('Course', secondary=courses_forums, back_populates='forums')