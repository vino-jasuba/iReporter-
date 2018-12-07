from marshmallow import Schema, fields, pre_dump
from app.api.utils.validator import required, latitude, longitude


class LocationSchema(Schema):
    lat = fields.Float(required=True, validate=(required, latitude))
    lng = fields.Float(required=True, valid=(required, longitude))


class IncidentSchema(Schema):
    """Represents the schema for incidents."""

    id = fields.Integer(required=False)
    incident_type = fields.Str(required=True, validate=(required))
    title = fields.Str(required=True, validate=(required))
    description = fields.Str(required=True, validate=(required))
    location = fields.Nested(LocationSchema, required=True)
    created_at = fields.DateTime(required=False,  format='%b, %d, %Y')

    @pre_dump
    def extract_location(self, data):
        location = {
            'lat': data['latitude'],
            'lng': data['longitude']
        }

        data['location'] = location

        return data
