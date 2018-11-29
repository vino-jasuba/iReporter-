import bcrypt
import re
from datetime import datetime
from flask import request
from flask_restful import Api, Resource, reqparse
from app.api.v1.common.api_response import ApiResponse
from .models import UserModel


class User(Resource, ApiResponse):

    def __init__(self):
        self.db = UserModel()

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
        self.db = UserModel()

    def get(self):
        return {
            'status': 200,
            'data': self.db.all()
        }, 200


class Register(Resource, ApiResponse):

    def __init__(self):
        self.db = UserModel()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'firstname', type=str, required=True, help='firstname field is required', location='json')
        self.reqparse.add_argument(
            'lastname', type=str, required=True, help='lastname field is required', location='json')
        self.reqparse.add_argument(
            'username', type=str, default="", help='username field is required', location='json')
        self.reqparse.add_argument(
            'email', type=str, required=True, help='email field is required', location='json')
        self.reqparse.add_argument(
            'password', type=str, required=True, help='password field is required', location='json')
        self.reqparse.add_argument(
            'password_confirm', type=str, required=True, help='password_confirm field is required', location='json')

    def post(self):
        data = request.get_json()

        # missing details will get updated on user profile
        data = self.reqparse.parse_args()
        print(data)
        if data['password'] != data['password_confirm']:
            return self.respondUnprocessibleEntity('passwords do not match')

        if not re.match(r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)", data['email']):
            return self.respondUnprocessibleEntity('email provided is not a valid email')

        if self.db.exists('email', data['email']):
            return self.respondUnprocessibleEntity('email already in use')

        if self.db.exists('username', data['username']):
            return self.respondUnprocessibleEntity('username already taken')
 
        user = {
            'firstname': data['firstname'],
            'lastname': data['lastname'],
            'othernames': None,
            'email': data['email'],
            'phoneNumber': None,
            'username': data['username'] if data['username'] else data['email'],
            'password': (bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())).decode('utf-8'),
            'registered': datetime.now().strftime('%c'),
            'isAdmin': False,
        }

        self.db.save(user)

        response = {'status': 201} 
        response.update(user)
        return response, 201    
