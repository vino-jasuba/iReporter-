import datetime
import os
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_mail import Message
from minio import Minio
from werkzeug.utils import secure_filename
from app.api.utils.api_response import ApiResponse
from app.api.v2.roles.roles import is_admin
from app.api.v2.users.models import UserModel
from app.api.v2.media.models import MediaModel
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

        data, errors = IncidentUpdateSchema(
            exclude=['status']).load(request.get_json())

        if errors:
            return self.respond({'message': 'failed to update record', 'errors': errors})

        if not data and errors:
            return self.respondUnprocessibleEntity({
                'message': 'at least one property required for update'
            })

        incident = self.db.find(incident_id)

        if not incident:
            return self.respondNotFound()

        if incident['created_by'] != get_jwt_identity()['id']:
            return self.respondUnauthorized('You do not have permission to update this record')

        incident = self.db.update(incident_id, data)
        incident = IncidentSchema().dump(incident)[0]

        return self.respond({'data': incident, 'message': 'successfully updated incident record'})

    @jwt_required
    def delete(self, incident_id):
        """remove resource with the given id from the model."""
        incident = self.db.find_or_fail(incident_id)

        if incident['created_by'] != get_jwt_identity()['id']:
            return self.respondUnauthorized('You do not have permission to update this record')

        self.db.delete(incident_id)

        message = 'record with id {} has been deleted'.format(incident_id)
        data = {'id': incident_id, 'message': message}
        return self.respond(data)


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

        if not is_admin(get_jwt_identity()):
            return self.respondUnauthorized('You do not have permission to perform this action')

        data, errors = IncidentUpdateSchema().load(data)

        if errors:
            self.respondUnprocessibleEntity({
                'errors': errors,
                'message': 'Invalid data received'
            })

        if data['status'] not in self.db.statuses:
            return self.respondUnprocessibleEntity('\'{}\' is not valid status')

        self.db.find_or_fail(incident_id)

        incident = self.db.update(incident_id, data)

        incident = IncidentSchema().dump(incident)[0]
        return self.respond({'data': incident, 'message': 'successfully updated record'})


class UserIncidents(Resource, ApiResponse):
    """Represents a Resource for fetching incident records created by the
    currently auth user
    """

    def __init__(self):
        self.db = IncidentModel()

    @jwt_required
    def get(self):
        user = get_jwt_identity()

        incident_records = self.db.where('created_by', user['id'])

        incident_records = IncidentSchema(many=True).dump(incident_records)[0]

        return self.respond({'data': incident_records})


class IncidentStatus(Resource, ApiResponse):
    """Represents a Resource for fetching list of statuses that an incident
    record can take
    """

    def get(self):
        return IncidentModel.statuses


class IncidentMedia(Resource, ApiResponse):
    """Represents a Resource for handling media belonging to an incident
    """

    def __init__(self):
        self.db = IncidentModel()

    @jwt_required
    def patch(self, incident_id):

        if not os.path.isdir('uploads'):
            os.mkdir('uploads')

        file = request.files['file']
        new_file_name = secure_filename(file.filename)
        file.save(os.path.join('uploads/', new_file_name))

        minioClient = Minio(
            os.getenv('STORAGE_URL'),
            access_key=os.getenv('MINIO_ACCESS_KEY'),
            secret_key=os.getenv('MINIO_SECRET_KEY'),
            secure=True
        )

        result = minioClient.fput_object(
            os.getenv('MINIO_BUCKET'),
            new_file_name,
            os.path.join('uploads/', new_file_name),
        )

        incident = self.db.find_or_fail(incident_id)

        media = MediaModel()

        media = media.save({
            'type': file.filename.rsplit('.', 1)[1].lower(),
            'handle': new_file_name,
            'object_id': str(result),
            'created_by': 1,
            'incident_id': incident['id'],
        })

        return self.respond({
            'data': IncidentUpdateSchema().dump(incident)[0]
        })
