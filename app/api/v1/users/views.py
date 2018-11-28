from flask import request
from flask_restful import Api, Resource
from app.api.v1.common.api_response import ApiResponse
from .models import UserModel

user_list = []

class User(Resource, ApiResponse):

    def __init__(self):
        self.db = UserModel(user_list)

    def get(self, user_id):
        user = self.db.find(user_id)

        if not user:
            return self.respondNotFound()

        return user, 200

    def patch(self, user_id):
        pass 

    def delete(self, user_id):
        pass 

        

class UserList(Resource, ApiResponse):

    def __init__(self):
        self.db = UserModel(user_list)

    def get(self):
        return {
            'status': 200,
            'data': self.db.all()
        }, 200 