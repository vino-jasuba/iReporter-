
from flask import request
from flask_restful import Api, Resource 
from .models import IncidentModel

class ApiResponse():

    def respondNotFound(self):
        return {'message': 'resource not found', 'status': 404}, 404

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
        self.db.delete(incident_id)

        return {'message': 'Successfully deleted record', 'status': 200}, 200

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
            'description': data['description']
        }

        self.db.save(incident)

        return {'message': 'Successfully created incident report'}, 201