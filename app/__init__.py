
from flask import Flask
from flask_restful import Api, Resource
from .api.v1.incidents.views import Incident, IncidentList, IncidenceQuery
from .api.v1.users.views import User, UserList
from .api.v1 import version_one as v1

def create_app():

    app = Flask(__name__)
    api = Api(v1)

    api.add_resource(Incident, '/incidents/<int:incident_id>')
    api.add_resource(IncidentList, '/incidents')
    api.add_resource(IncidenceQuery, '/incidents/<string:incident_type>')
    api.add_resource(User, '/users/<int:user_id>')
    api.add_resource(UserList, '/user')
    app.register_blueprint(v1)

    return app