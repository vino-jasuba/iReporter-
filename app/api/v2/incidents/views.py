import datetime
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from app.api.utils.api_response import ApiResponse
from .models import IncidentModel
from .schema import IncidentSchema


class Incident(Resource, ApiResponse):
    """Represents a resource class used to interact with incident reports 
    through HTTP methods."""

    def __init__(self):
        """Initialize resource with a reference to the model it should use."""

        self.db = IncidentModel()

    @jwt_required
    def get(self, incident_id):
        """get a resource by id from the model."""
        incident = self.db.find(incident_id)

        if not incident:
            return self.respondNotFound()

        return IncidentSchema().dump(incident)[0], 200

    @jwt_required
    def patch(self, incident_id):
        """update resource with the given id."""

        incident = self.db.find(incident_id)

        if not incident:
            return self.respondNotFound()

        incident = self.db.update(incident_id, request.get_json())

        return IncidentSchema().dump(incident)[0], 200

    @jwt_required
    def delete(self, incident_id):
        """remove resource with the given id from the model."""

        deleted_record = self.db.delete(incident_id)

        if deleted_record:
            return {
                       'data': [{
                           'id': incident_id,
                           'message': 'record has been deleted'
                       }],
                       'status': 200
                   }, 200
        else:
            return self.respondNotFound()


class IncidentList(Resource):
    """Represents a resource class used to interact with incident 
    reports through through HTTP methods."""

    def __init__(self):
        """Initialize resource with a reference to the model it should use."""

        self.db = IncidentModel()

    @jwt_required
    def get(self):
        """Fetch a list of all records from the model."""

        return {
                   'status': 200,
                   'data': IncidentSchema(many=True).dump(self.db.all())[0]
               }, 200

    @jwt_required
    def post(self):
        """Create new incident records. The method also performs validation 
        to ensure all fields required are present.
        """
        user = get_jwt_identity()

        data, errors = IncidentSchema().load(request.get_json())

        if errors:
            return {'errors': errors, 'message': 'Invalid data received', 'status': 422}, 422

        incident = {
            'incident_type': data['incident_type'],
            'title': data['title'],
            'images': [],
            'videos': [],
            'description': data['description'],
            'location': {
                'lat': data['location']['lat'],
                'lng': data['location']['lng']
            },
            'created_on': datetime.datetime.now().strftime('%c'),
            'created_by': user['id']
        }

        self.db.save(incident)

        return {'message': 'Successfully created incident report'}, 201


class IncidenceQuery(Resource):
    """Represents a resource class used to interact with incident
    reports through HTTP methods. It exposes a method for fetching incident records 
    by the given type string."""

    def __init__(self):
        """Initialize resource with a reference to the model it should use."""

        self.db = IncidentModel()

    @jwt_required
    def get(self, incident_type):
        red_flags = self.db.where('incident_type', incident_type)

        return {
            'data': IncidentSchema(many=True).dump(red_flags)[0],
            'status': 200
        }


class IncidentManager(Resource, ApiResponse):
    """Represents a resource class used by admin user to manage incident
        reports through HTTP methods. It exposes a method for updating the status on incident records
    """

    def __init__(self):
        """Initialize resource with a reference to the model it should use."""

        self.db = IncidentModel()

    @jwt_required
    def patch(self, incident_id):
        """Update the status of an incident record"""
        data = request.get_json()

        if data['status'] not in self.db.statuses:
            return self.respondUnprocessibleEntity('Not valid status')

        incident = self.db.find(incident_id)

        if not incident:
            return self.respondNotFound()

        incident = self.db.update(incident_id, data)

        return IncidentSchema().dump(incident)[0]
