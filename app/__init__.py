import os
from flask_jwt_extended import JWTManager
from flask import Flask, Blueprint
from .api.v1 import version_one as v1
from instance.config import app_config


def create_app(config_name):
    """create a new instance of a flask app using given config.
    returns a reference to the created app."""

    app = Flask(__name__)
    app.register_blueprint(v1)
    app.config.from_object(app_config[config_name])
    JWTManager(app)
    return app
