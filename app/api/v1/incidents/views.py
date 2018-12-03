import datetime
from flask import request
from flask_restful import Api, Resource
from marshmallow import Schema, fields
from app.api.v1.common.api_response import ApiResponse
from app.api.v1.common.validator import required
from .models import IncidentModel


class IncidentSchema(Schema):
    incident_type = fields.Str(required=True, validate=(required))
    title = fields.Str(required=True, validate=(required))
    description = fields.Str(required=True, validate=(required))
    location = fields.Dict(required=True, validate=(required))


class Incident(Resource, ApiResponse):

    def __init__(self):
        self.db = IncidentModel()

    def get(self, incident_id):
        incident = self.db.find(incident_id)

        if not incident:
            return self.respondNotFound()

        return incident, 200

    def patch(self, incident_id):
        incident = self.db.find(incident_id)

        if not incident:
            return self.respondNotFound()

        self.db.update(incident, request.get_json())

        return incident, 200

    def delete(self, incident_id):
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

    def __init__(self):
        self.db = IncidentModel()

    def get(self):
        return {
            'status': 200,
            'data': self.db.all()
        }, 200

    def post(self):

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


class IncidenceQuery(Incident):

    def get(self, incident_type):
        red_flags = self.db.where('incident_type', incident_type).get()

        return {
            'data': red_flags,
            'status': 200
        }
