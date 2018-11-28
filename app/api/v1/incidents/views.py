
from flask import request
from flask_restful import Api, Resource 
from app.api.v1.common.api_response import ApiResponse
from .models import IncidentModel

incident_list = []

class IncidentList(Resource):
    
    def __init__(self):
        self.db = IncidentModel(incident_list)

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


