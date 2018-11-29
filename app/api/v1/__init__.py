from flask_restful import Api, Resource
from flask import Blueprint
from .incidents.views import Incident, IncidentList, IncidenceQuery
from .users.views import User, UserList
 
version_one = Blueprint('api_v1', __name__, url_prefix='/api/v1')

api = Api(version_one)

api.add_resource(Incident, '/incidents/<int:incident_id>')
api.add_resource(IncidentList, '/incidents')
api.add_resource(IncidenceQuery, '/incidents/<string:incident_type>')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserList, '/users')