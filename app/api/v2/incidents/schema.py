from marshmallow import Schema, fields, pre_dump
from app.api.utils.validator import not_empty, latitude, longitude, valid_type


class LocationSchema(Schema):
    lat = fields.Float(required=True, validate=(not_empty, latitude),
                       error_messages={'validator_failed': 'invalid latitude coordinate'})
    lng = fields.Float(required=True, validate=(not_empty, longitude),
                       error_messages={'validator_failed': 'invalid longitude coordinate'})
    # city = fields.Str(required=True, validate=(not_empty),
    #                   error_messages={'validator_failed': 'you should provide a city'})


class IncidentSchema(Schema):
    """Represents the schema for incidents."""

    id = fields.Integer(required=False)
    incident_type = fields.Str(required=True, validate=(not_empty, valid_type))
    title = fields.Str(required=True, validate=(not_empty))
    description = fields.Str(required=True, validate=(not_empty))
    location = fields.Nested(LocationSchema, required=True)
    status = fields.Str(required=False, validate=(not_empty))
    created_at = fields.DateTime(required=False, format='%b, %d, %Y')

    @pre_dump
    def extract_location(self, data):
        location = {
            'lat': data['latitude'],
            'lng': data['longitude']
        }

        data['location'] = location

        return data


class IncidentUpdateSchema(IncidentSchema):
    """Represents the schema for updating incidents"""
    incident_type = fields.Str(required=False, validate=(not_empty, valid_type))
    title = fields.Str(required=False, validate=(not_empty))
    description = fields.Str(required=False, validate=(not_empty))
    location = fields.Nested(LocationSchema, required=False,
                             error_messages={'validator_failed': 'invalid coordinate data found in request'})
    status = fields.Str(required=False, validate=(not_empty))
