
from flask import Flask, Blueprint
from .api.v1 import version_one as v1


def create_app(config_name):
    """create a new instance of a flask app using given config.
    returns a reference to the created app."""

    app = Flask(__name__)
    app.register_blueprint(v1)
    return app
