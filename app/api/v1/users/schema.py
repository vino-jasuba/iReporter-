from marshmallow import Schema, fields, post_dump
from app.api.utils.validator import not_empty, strong_password


class UserSchema(Schema):
    """Represents the schema for users."""

    firstname = fields.Str(required=True, validate=(not_empty))
    lastname = fields.Str(required=True, validate=(not_empty))
    username = fields.Str(required=True, validate=(not_empty))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=(not_empty, strong_password))

    @post_dump
    def add_id(self, data):

        users = self.context.get('users', None)

        if users:
            for user in users:
                data['id'] = user['id']

            return data

        return data
