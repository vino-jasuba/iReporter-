
from flask import Flask
from flask_restful import Api, Resource
from .api.v1.incidents.views import IncidentList
from .api.v1 import version_one as v1

def create_app():

    app = Flask(__name__)
    api = Api(v1)

    api.add_resource(IncidentList, '/incidents')
    app.register_blueprint(v1)

    return app