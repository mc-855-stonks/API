from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.main.config import config_by_env
from redis import Redis

redis = Redis(host='localhost', port=6379, db=0)
db = SQLAlchemy()
flask_bcrypt = Bcrypt()

def create_app(env):
    app = Flask(__name__)
    app.config.from_object(config_by_env[env])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app