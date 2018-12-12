from marshmallow import Schema, fields

from app.api.utils.validator import not_empty, strong_password


class UserSchema(Schema):
    """Represents the schema for users."""

    id = fields.Integer(required=False)
    firstname = fields.Str(required=True, validate=(not_empty))
    lastname = fields.Str(required=True, validate=(not_empty))
    username = fields.Str(required=True, validate=(not_empty))
    othernames = fields.Str(required=False)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=(not_empty, strong_password))
    registered = fields.DateTime(required=False, format='%b, %d, %Y')
