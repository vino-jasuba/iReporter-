from marshmallow import Schema, fields, pre_dump, pre_load
from app.api.utils.validator import not_empty, strong_password
from psycopg2.extras import RealDictCursor
from flask import g


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
    isAdmin = fields.Bool(required=False)

    @pre_dump
    def role(self, data):
        role = data['role']

        conn = g.conn
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM roles WHERE id = {}".format(role))
        role = cursor.fetchone()

        if role['role_slug'] == 'admin':
            data['isAdmin'] = True
        else:
            data['isAdmin'] = False

        return data
