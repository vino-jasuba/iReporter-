from flask import Blueprint
from flask_restful import Api
from .incidents.views import (Incident, IncidentList, IncidenceQuery,
                              IncidentManager, UserIncidents, IncidentStatus)
from .users.views import User, UserList, Register, Login, UserProfile

version_two = Blueprint('api_v2', __name__, url_prefix='/api/v2')

api = Api(version_two, catch_all_404s=True)

api.add_resource(Incident, '/incidents/<int:incident_id>')
api.add_resource(IncidentList, '/incidents')
api.add_resource(IncidenceQuery, '/incidents/<string:incident_type>')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(UserProfile, '/auth/user/profile')
api.add_resource(UserIncidents, '/users/incidents')
api.add_resource(IncidentStatus, '/statuses')
api.add_resource(Register, '/auth/signup')
api.add_resource(Login, '/auth/login')
api.add_resource(IncidentManager, '/admin/incidents/<int:incident_id>')
