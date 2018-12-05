from marshmallow import Schema, fields
from app.api.v1.common.validator import required, email


class UserSchema(Schema):
    """Represents the schema for users."""

    firstname = fields.Str(required=True, validate=(required))
    lastname = fields.Str(required=True, validate=(required))
    username = fields.Str(required=True, validate=(required))
    email = fields.Email(required=True, validate=(email))
    password = fields.Str(required=True, validate=(required))
    password_confirm = fields.Str(required=True, validate=(required))
