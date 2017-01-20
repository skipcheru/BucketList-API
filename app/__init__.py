from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    from .auth.views import auth
    app.register_blueprint(auth)

    from .bucketlist.views import bucketlists
    app.register_blueprint(bucketlists)

    return app
