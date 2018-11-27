
from flask import Flask
from flask_restful import Api, Resource
from .api.v1.views import Incident, IncidentList
from .api.v1 import version_one as v1

def create_app():

    app = Flask(__name__)
    api = Api(v1)

    api.add_resource(Incident, '/red-flags/<int:red_flag_id>')
    api.add_resource(IncidentList, '/red-flags')
    app.register_blueprint(v1)

    return app