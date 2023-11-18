from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Import your blueprints
from .main.routes import main
from .auth.routes import auth
from .courses.routes import courses
from .forum.routes import forum
from .tutoring.routes import tutoring
from .user.routes import user
from .extensions import db, login_manager, migrate
import os
from . import models
basedir = os.path.abspath(os.path.dirname(__file__))

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] =     'sqlite:///' + os.path.join(basedir, 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   
    app.config['SECRET_KEY'] = "CringeCode" 
    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(courses, url_prefix='/courses')
    app.register_blueprint(forum, url_prefix='/forum')
    app.register_blueprint(tutoring, url_prefix='/tutoring')
    app.register_blueprint(user, url_prefix='/user')

    return app
