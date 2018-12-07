from marshmallow import Schema, fields, post_dump
from app.api.utils.validator import required, email, strong_password


class UserSchema(Schema):
    """Represents the schema for users."""

    id = fields.Integer(required=False)
    firstname = fields.Str(required=True, validate=(required))
    lastname = fields.Str(required=True, validate=(required))
    username = fields.Str(required=True, validate=(required))
    othernames = fields.Str(required=False)
    email = fields.Email(required=True, validate=(email))
    password = fields.Str(required=True, validate=(required, strong_password))
    password_confirm = fields.Str(required=True, validate=(required))
    registered = fields.DateTime(required=False, format='%b, %d, %Y')
