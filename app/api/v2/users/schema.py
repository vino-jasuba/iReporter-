from marshmallow import Schema, fields, post_dump
from app.api.utils.validator import required, email, strong_password


class UserSchema(Schema):
    """Represents the schema for users."""

    firstname = fields.Str(required=True, validate=(required))
    lastname = fields.Str(required=True, validate=(required))
    username = fields.Str(required=True, validate=(required))
    email = fields.Email(required=True, validate=(email))
    password = fields.Str(required=True, validate=(required))
    password_confirm = fields.Str(required=True, validate=(required))

    @post_dump
    def add_id(self, data):

        users = self.context.get('users', None)

        if users:
            for user in users:
                data['id'] = user['id']

            return data

        return data
