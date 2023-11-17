from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from .main.routes import main
# Initialize the extensions
#db = SQLAlchemy()
#login_manager = LoginManager()
#login_manager.login_view = 'auth.login'
#migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app context
    #db.init_app(app)
    #login_manager.init_app(app)
    #migrate.init_app(app, db)

    # Import and register blueprints
    app.register_blueprint(main)

    #from app.auth import auth as auth_blueprint
    #app.register_blueprint(auth_blueprint, url_prefix='/auth')

    #from app.courses import courses as courses_blueprint
    #app.register_blueprint(courses_blueprint, url_prefix='/courses')

    #from app.forum import forum as forum_blueprint
    #app.register_blueprint(forum_blueprint, url_prefix='/forum')

    #from app.tutoring import tutoring as tutoring_blueprint
    #app.register_blueprint(tutoring_blueprint, url_prefix='/tutoring')

    #from app.errors import errors as errors_blueprint
    #app.register_blueprint(errors_blueprint)

    # Return the app instance
    return app
