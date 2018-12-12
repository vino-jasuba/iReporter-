from flask import Flask
from flask_jwt_extended import JWTManager

from app.api.v1 import version_one as v1
from app.api.v2 import version_two as v2
from instance.config import app_config


def create_app(config_name):
    """create a new instance of a flask app using given config.
    returns a reference to the created app."""

    app = Flask(__name__)
    app.register_blueprint(v1)
    app.register_blueprint(v2)
    app.config.from_object(app_config[config_name])
    JWTManager(app)
    return app
