from marshmallow import Schema, fields
from app.api.utils.validator import required, geopoint


class IncidentSchema(Schema):
    """Represents the schema for incidents."""

    incident_type = fields.Str(required=True, validate=(required))
    title = fields.Str(required=True, validate=(required))
    description = fields.Str(required=True, validate=(required))
    location = fields.Dict(required=True, validate=(
        required, geopoint))
