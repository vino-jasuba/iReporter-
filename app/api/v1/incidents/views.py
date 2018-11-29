
from flask import request
from flask_restful import Api, Resource 
from app.api.v1.common.api_response import ApiResponse
from .models import IncidentModel

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

        incident.update(request.get_json())

        return incident, 200 

    def delete(self, incident_id):
        deleted_record = self.db.delete(incident_id)

        if deleted_record:
            return {
                'data': [{
                    'id': deleted_record['id'],
                    'message': deleted_record['type'] + ' ' + ' has been deleted'
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

        data = request.get_json()

        incident = {
            'type': data['type'],
            'title': data['title'],
            'images': [],
            'description': data['description'],
            'location': {
                'lat': data['location']['lat'],
                'lng': data['location']['lng']
            }
        }

        self.db.save(incident)

        return {'message': 'Successfully created incident report'}, 201



class IncidenceQuery(Incident):

    def get(self, incident_type):
        red_flags = self.db.where('type', incident_type).get()

        return {
            'data': red_flags,
            'status': 200
        }
