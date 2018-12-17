from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from psycopg2 import Error
from flask_cors import CORS

from app.api.v1 import version_one as v1
from app.api.v2 import version_two as v2
from instance.config import app_config
from app.api.utils.databasemodel import ModelNotFound


@v2.app_errorhandler(Exception)
def handle_error(error):
    response = None
    status_code = 500

    if isinstance(error, Error):
        response = {
            'message': 'Database error. Could not complete requested database transaction.',
        }

        status_code = 404
    elif isinstance(error, ModelNotFound):
        response = {
            'message': 'resource not found'
        }

        status_code = 404

    elif isinstance(error, Exception):
        response = {
            'message': 'Could not complete your request'
        }
        status_code = 400

    response.update({'status': status_code})

    return jsonify(response), status_code


def create_app(config_name):
    """create a new instance of a flask app using given config.
    returns a reference to the created app."""

    app = Flask(__name__)
    app.register_blueprint(v1)
    app.register_blueprint(v2)
    app.config.from_object(app_config[config_name])
    JWTManager(app)
    CORS(app)

    return app
