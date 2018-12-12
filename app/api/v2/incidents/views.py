import datetime
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from app.api.utils.api_response import ApiResponse
from .models import IncidentModel
from .schema import IncidentSchema, IncidentUpdateSchema


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

        incident = IncidentSchema().dump(incident)[0]

        return self.respond({'data': incident})

    @jwt_required
    def patch(self, incident_id):
        """update resource with the given id."""

        data, errors = IncidentUpdateSchema().load(request.get_json())

        if errors:
            return self.respond({'message': 'failed to update record', 'errors': errors})

        if not data and errors:
            return self.respondUnprocessibleEntity({
                'message': 'at least one property required for update'
            })

        incident = self.db.find(incident_id)

        if not incident:
            return self.respondNotFound()

        incident = self.db.update(incident_id, data)
        incident = IncidentSchema().dump(incident)[0]

        return self.respond({'data': incident, 'message': 'successfully updated incident record'})

    @jwt_required
    def delete(self, incident_id):
        """remove resource with the given id from the model."""

        deleted_record = self.db.delete(incident_id)

        if deleted_record:
            message = 'record with id {} has been deleted'.format(incident_id)
            data = {'id': incident_id, 'message': message}
            return self.respond(data)
        else:
            return self.respondNotFound()


class IncidentList(Resource, ApiResponse):
    """Represents a resource class used to interact with incident 
    reports through through HTTP methods."""

    def __init__(self):
        """Initialize resource with a reference to the model it should use."""

        self.db = IncidentModel()

    @jwt_required
    def get(self):
        """Fetch a list of all records from the model."""

        data = IncidentSchema(many=True).dump(self.db.all())[0]

        return self.respond({'data': data})

    @jwt_required
    def post(self):
        """Create new incident records. The method also performs validation 
        to ensure all fields required are present.
        """
        user = get_jwt_identity()

        data, errors = IncidentSchema().load(request.get_json())

        if errors:
            return self.respondUnprocessibleEntity({
                'errors': errors,
                'message': 'Invalid data received'
            })

        data.update({'created_by': user['id']})
        data = self.db.save(data)
        data = IncidentSchema().dump(data)[0]

        return self.respondEntityCreated({'data': data, 'message': 'successfully created incident record'})


class IncidenceQuery(Resource, ApiResponse):
    """Represents a resource class used to interact with incident
    reports through HTTP methods. It exposes a method for fetching incident records 
    by the given type string."""

    def __init__(self):
        """Initialize resource with a reference to the model it should use."""

        self.db = IncidentModel()

    @jwt_required
    def get(self, incident_type):
        incident_records = self.db.where('incident_type', incident_type)

        incident_records = IncidentSchema(many=True).dump(incident_records)[0]

        return self.respond({'data': incident_records})


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
            return self.respondUnprocessibleEntity('\'{}\' is not valid status')

        incident = self.db.find(incident_id)

        if not incident:
            return self.respondNotFound()

        incident = self.db.update(incident_id, data)
        incident = IncidentSchema().dump(incident)[0]
        return self.respond({'data': incident, 'message': 'successfully updated record'})


class UserIncidents(Resource, ApiResponse):

    def __init__(self):
        self.db = IncidentModel()

    @jwt_required
    def get(self):

        user = get_jwt_identity()

        incident_records = self.db.where('created_by', user['id'])

        incident_records = IncidentSchema(many=True).dump(incident_records)[0]
        
        return self.respond({'data': incident_records})


