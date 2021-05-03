from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.main.config import config_by_env
from flask_cors import CORS

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

def create_app(env):
    app = Flask(__name__)
    app.config.from_object(config_by_env[env])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    CORS(app, allow_headers='Content-Type', expose_headers='*, Authorization')

    return app