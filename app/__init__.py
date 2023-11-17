from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from .main.routes import main
from .auth.routes import auth
from .courses.routes import courses
from .forum.routes import forum
from .tutoring.routes import tutoring
from .user.routes import user


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
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(courses, url_prefix='/courses')
    app.register_blueprint(forum, url_prefix='/forum')
    app.register_blueprint(tutoring, url_prefix='/tutoring')
    app.register_blueprint(user, url_prefix='/user')


    #app.register_blueprint(errors_blueprint)

    # Return the app instance
    return app
