import datetime
from flask import request
from flask_restful import Api, Resource
from app.api.utils.api_response import ApiResponse
from app.api.utils.validator import not_empty
from .models import IncidentModel
from .schema import IncidentSchema
from flask_jwt_extended import jwt_required


class Incident(Resource, ApiResponse):
    """Represents a resource class used to interact with incident reports 
    through HTTP methods."""

    def __init__(self):
        """Initialize resource with a reference to the model it should use."""

        self.db = IncidentModel()

    def get(self, incident_id):
        """get a resource by id from the model."""

        incident = self.db.find(incident_id)

        if not incident:
            return self.respondNotFound()

        return incident, 200

    def patch(self, incident_id):
        """update resource with the given id."""

        incident = self.db.find(incident_id)

        if not incident:
            return self.respondNotFound()

        self.db.update(incident, request.get_json())

        return incident, 200

    def delete(self, incident_id):
        """remove resource with the given id from the model."""

        deleted_record = self.db.delete(incident_id)

        if deleted_record:
            return {
                'data': [{
                    'id': deleted_record['id'],
                    'message': deleted_record['incident_type'] + ' ' + ' has been deleted'
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

    def get(self):
        """Fetch a list of all records from the model."""

        return {
            'status': 200,
            'data': self.db.all()
        }, 200

    def post(self):
        """Create new incident records. The method also performs validation 
        to ensure all fields required are present.
        """

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
            'created_by': None  # we'll need an authenticated user for this
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

    def get(self, incident_type):
        red_flags = self.db.where('incident_type', incident_type).get()

        return {
            'data': red_flags,
            'status': 200
        }
