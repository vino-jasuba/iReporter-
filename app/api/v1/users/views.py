import bcrypt
import re
from datetime import datetime
from flask import request
from marshmallow import ValidationError, Schema, fields
from flask_restful import Api, Resource, reqparse
from app.api.v1.common.api_response import ApiResponse
from app.api.v1.common.validator import email, required
from .models import UserModel

class UserSchema(Schema):
    """Represents the schema for users."""

    firstname = fields.Str(required=True, validate=(required))
    lastname = fields.Str(required=True, validate=(required))
    username = fields.Str(required=True, validate=(required))
    email = fields.Email(required=True, validate=(email))
    password = fields.Str(required=True, validate=(required))
    password_confirm = fields.Str(required=True, validate=(required))


class UserSchema(Schema):
    """Represents the schema for users."""

    firstname = fields.Str(required=True, validate=(required))
    lastname = fields.Str(required=True, validate=(required))
    username = fields.Str(required=True, validate=(required))
    email = fields.Email(required=True, validate=(email))
    password = fields.Str(required=True, validate=(required))
    password_confirm = fields.Str(required=True, validate=(required))


class User(Resource, ApiResponse):
    """Represents a resource class used to interact with user resource
    through HTTP methods. It exposes methods for fetching, updating and deleting items
    with given ids."""

    def __init__(self):
        """Initialize resource with a reference to the model it should use."""

        self.db = UserModel()

    def get(self, user_id):
        """get a user resource by id from the model."""

        user = self.db.find(user_id)

        if not user:
            return self.respondNotFound()

        return user, 200

    def patch(self, user_id):
        """update user resource with the given id."""

        user = self.db.find(user_id)

        if not user:
            return self.respondNotFound()

        self.db.update(user, request.get_json())

        return user, 200

    def delete(self, user_id):
        """remove resource with given id from the data store."""

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
    """Represents a resource class used to interact with users 
    through HTTP methods. Exposes methods for fetching entire 
    list of users."""

    def __init__(self):
        """Initialize resource with a reference to the model it should use."""

        self.db = UserModel()

    def get(self):
        """fetch all users from the data store."""

        return {
            'status': 200,
            'data': self.db.all()
        }, 200


class Register(Resource, ApiResponse):
    """Represents a resource class used to register new users.
    Exposes methods for registering new users."""

    def __init__(self):
        """Initialize model that the resource should use as well
        as the schema it should use for validation."""

        self.db = UserModel()
        self.schema = UserSchema()

    def post(self):
        """register a new user."""

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

        response = UserSchema(exclude=['password']).dump(user)[0]
        return response, 201


class Login(Resource, ApiResponse):
    """Represents a resource class used to register new users.
    Exposes methods for registering new users."""

    def __init__(self):
        """Initialize resource with a reference to the model it should use."""

    def post(self):
        """login a user with given credentials"""
        # TODO: implement jwt auth 

        pass