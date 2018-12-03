import bcrypt
import re
from datetime import datetime
from flask import request
from marshmallow import ValidationError, Schema, fields
from flask_restful import Api, Resource, reqparse
from app.api.v1.common.api_response import ApiResponse
from .models import UserModel


class UserSchema(Schema):
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    password_confirm = fields.Str(required=True)


class User(Resource, ApiResponse):

    def __init__(self):
        self.db = UserModel()

    def get(self, user_id):
        user = self.db.find(user_id)

        if not user:
            return self.respondNotFound()

        return user, 200

    def patch(self, user_id):
        user = self.db.find(user_id)

        if not user:
            return self.respondNotFound()

        self.db.update(user, request.get_json())

        return user, 200

    def delete(self, user_id):

        deleted_record = self.db.delete(user_id)

        if deleted_record:
            return {
                'data': [{
                    'id': deleted_record['id'],
                    'message': 'user with id {}'.format(deleted_record['id']) + ' has been deleted'
                }],
                'status': 200
            }, 200
        else:
            return self.respondNotFound()


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
        self.schema = UserSchema()

    def post(self):
        data = request.get_json()
        schema = UserSchema()

        data, errors = schema.load(data)

        if errors:
            return {'errors': errors, 'message': 'Invalid data received', 'status': 422}, 422

        if self.db.exists('username', data['username']):
            return self.respondUnprocessibleEntity('username already taken')

        if self.db.exists('email', data['email']):
            return self.respondUnprocessibleEntity('email already in use')

        user = {
            'firstname': data['firstname'],
            'lastname': data['lastname'],
            'othernames': None,
            'email': data['email'],
            'phoneNumber': None,
            'username': data['username'] if data['username'] else data['email'],
            'password': (bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())).decode('utf-8'),
            'registered': datetime.now().strftime('%c'),
            'isAdmin': False
        }

        self.db.save(user)

        response = UserSchema(only=('firstname', 'lastname', 'othernames',
                                    'email', 'phoneNumber', 'username', 'registered', 'isAdmin')).dump(user)[0]
        return response, 201
