from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
)
# from app.config import settings
import logging

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    app.secret_key = 'secret-key'
    app.logger.setLevel(logging.INFO)

    login_manager.init_app(app)
    bcrypt.init_app(app)

    return app