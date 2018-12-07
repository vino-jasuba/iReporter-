import re
from datetime import datetime
from flask import request
from flask_restful import Api, Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from app.api.utils.api_response import ApiResponse
from app.api.utils.validator import email, required
from .models import UserModel
from .schema import UserSchema

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required


class User(Resource, ApiResponse):
    """Represents a resource class used to interact with user resource
    through HTTP methods. It exposes methods for fetching, updating and deleting items
    with given ids."""

    def __init__(self):
        """Initialize resource with a reference to the model it should use."""

        self.db = UserModel()

    # @jwt_required
    def get(self, user_id):
        """get a user resource by id from the model."""

        user = self.db.find(user_id)

        if not user:
            return self.respondNotFound()

        return UserSchema(exclude=['password']).dump(user)[0], 200

    # @jwt_required
    def patch(self, user_id):
        """update user resource with the given id."""

        user = self.db.find(user_id)

        if not user:
            return self.respondNotFound()

        self.db.update(user_id, request.get_json())

        return UserSchema(exclude=['password']).dump(self.db.find(user_id))[0], 200

    # @jwt_required
    def delete(self, user_id):
        """remove resource with given id from the data store."""

        deleted_record = self.db.delete(user_id)

        if deleted_record:
            return {
                'data': [{
                    'id': user_id,
                    'message': 'user with id {}'.format(user_id) + ' has been deleted'
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

    # @jwt_required
    def get(self):
        """fetch all users from the data store."""

        return {
            'status': 200,
            'data': UserSchema(many=True, exclude=['password']).dump(self.db.all())[0]
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
            'password': generate_password_hash(data['password']),
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
        self.db = UserModel()

    def post(self):
        """login a user with given credentials"""

        data = request.get_json()
        schema = UserSchema()

        data, errors = schema.load(data, partial=(
            'email', 'firstname', 'lastname', 'password_confirm'))
        
        if errors:
            return {'message': 'Weak password', 'errors': errors}, 422

        users = self.db.where('username', data['username'])

        if not users:
            return self.respondNotFound()

        user = users[0]

        if check_password_hash(user['password'], data['password']):
            return {
                'access_token': create_access_token(UserSchema(exclude=['password']).dump(user)[0]),
                'refresh_token': create_refresh_token(UserSchema(exclude=['password']).dump(user)[0])
            }

        return self.respondUnauthorized('We do not have a user with the provided credentials')
