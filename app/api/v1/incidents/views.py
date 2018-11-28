
from flask import request
from flask_restful import Api, Resource 
from app.api.v1.common.api_response import ApiResponse
from .models import IncidentModel

incident_list = [] 

class Incident(Resource, ApiResponse):
    
    def __init__(self):
        self.db = IncidentModel(incident_list)

    
    def get(self, incident_id):
        incident = self.db.find(incident_id)

        if not incident:
            return self.respondNotFound()
        
        return incident, 200
        

class IncidentList(Resource):
    
    def __init__(self):
        self.db = IncidentModel(incident_list)
    
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
