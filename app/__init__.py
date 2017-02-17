from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

from app.auth.views import auth, jwt
from app.bucketlist.views import bucketlists


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(bucketlists)

    return app
