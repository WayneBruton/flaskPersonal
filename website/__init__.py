import os
from os import path

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")


# if website/uploads folder does not exist, create it


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config['UPLOAD_FOLDER'] = 'uploads'
    db.init_app(app)

    # app.static_url_path = '/static'
    # app.static_folder = 'static'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    # login_manager.login_message = 'You must be logged in to access this page.'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("instance/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created Database!")
    else:
        print("Database already exists!")
