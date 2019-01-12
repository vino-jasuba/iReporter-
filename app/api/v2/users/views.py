from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from app.api.utils.api_response import ApiResponse
from app.api.v2.roles.roles import is_admin
from .models import UserModel
from .schema import UserSchema


class User(Resource, ApiResponse):
    """Represents a resource class used to interact with user resource
    through HTTP methods. It exposes methods for fetching, updating and deleting items
    with given ids."""

    def __init__(self):
        """Initialize resource with a reference to the model it should use."""

        self.db = UserModel()

    @jwt_required
    def get(self, user_id):
        """get a user resource by id from the model."""

        user = self.db.find(user_id)

        if not user:
            return self.respondNotFound()

        user = UserSchema(exclude=['password']).dump(user)[0]
        return self.respond({'data': user})

    @jwt_required
    def patch(self, user_id):
        """update user resource with the given id."""

        user = self.db.find(user_id)

        if not user:
            return self.respondNotFound()

        user = self.db.update(user_id, request.get_json())
        user = UserSchema(exclude=['password']).dump(user)[0]

        return self.respond({'data': user, 'message': 'successfully updated user details'})

    @jwt_required
    def delete(self, user_id):
        """remove resource with given id from the data store."""

        deleted_record = self.db.delete(user_id)

        if deleted_record:
            message = 'user with id {}'.format(user_id) + ' has been deleted'
            data = {'id': user_id, 'message': message}
            return self.respond(data)
        else:
            return self.respondNotFound()


class UserProfile(Resource, ApiResponse):
    """Represents a resource class used to interact with
    auth users
    """

    @jwt_required
    def get(self):
        user = get_jwt_identity()

        return user


class UserList(Resource, ApiResponse):
    """Represents a resource class used to interact with users 
    through HTTP methods. Exposes methods for fetching entire 
    list of users."""

    def __init__(self):
        """Initialize resource with a reference to the model it should use."""

        self.db = UserModel()

    @jwt_required
    def get(self):
        """fetch all users from the data store."""

        data = UserSchema(many=True, exclude=['password']).dump(self.db.all())[0]
        return self.respond({'data': data})


class Register(Resource, ApiResponse):
    """Represents a resource class used to register new users.
    Exposes methods for registering new users."""

    def __init__(self):
        """Initialize model that the resource should use as well
        as the schema it should use for validation."""

        self.db = UserModel()

    def post(self):
        """register a new user."""

        data, errors = UserSchema().load(request.get_json())

        if errors:
            return self.respondUnprocessibleEntity({
                'errors': errors,
                'message': 'Invalid data received'
            })

        if self.db.exists('username', data['username']):
            return self.respondUnprocessibleEntity({
                'message': 'username already taken'
            })

        if self.db.exists('email', data['email']):
            return self.respondUnprocessibleEntity({'message': 'email already in use'})

        user = {
            'firstname': data['firstname'],
            'lastname': data['lastname'],
            'othernames': "",
            'email': data['email'],
            'phoneNumber': "",
            'username': data['username'] if data['username'] else data['email'],
            'password': generate_password_hash(data['password']),
        }

        user = self.db.save(user)

        response = UserSchema(exclude=['password']).dump(user)[0]
        return self.respondEntityCreated({'data': response, 'message': 'Successfully created user'})


class Login(Resource, ApiResponse):
    """Represents a resource class used to register new users.
    Exposes methods for registering new users."""

    def __init__(self):
        """Initialize resource with a reference to the model it should use."""
        self.db = UserModel()

    def post(self):
        """login a user with given credentials"""

        # take advantage of UserSchema password side effect
        data, errors = UserSchema(only=('username', 'password')).load(request.get_json())

        auth_failure_message = 'Username or password not valid'

        if errors:
            return self.respondUnprocessibleEntity({
                'message': auth_failure_message
            })

        users = self.db.where('username', data['username'])

        if not users:
            return self.respondUnauthorized(auth_failure_message)

        user = users[0]

        if check_password_hash(user['password'], data['password']):
            return self.respond({
                'access_token': create_access_token(UserSchema(exclude=['password']).dump(user)[0],
                                                    expires_delta=False),
                'refresh_token': create_refresh_token(UserSchema(exclude=['password']).dump(user)[0]),
                'message': 'successfully authenticated user'
            })

        return self.respondUnauthorized(auth_failure_message)
