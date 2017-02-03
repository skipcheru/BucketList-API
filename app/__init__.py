from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_jwt import JWT

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    jwt = JWT(app, authenticate, identity)

    db.init_app(app)
    jwt.init_app(app)

    from app.auth.views import auth
    app.register_blueprint(auth)

    from app.bucketlist.views import bucketlists
    app.register_blueprint(bucketlists)

    return app

from app.auth.validate import authenticate, identity, jwt

jwt = JWT(create_app('default'), authenticate, identity)
