from marshmallow import Schema, fields
from app.api.v1.common.validator import required

class IncidentSchema(Schema):
    """Represents the schema for incidents."""

    incident_type = fields.Str(required=True, validate=(required))
    title = fields.Str(required=True, validate=(required))
    description = fields.Str(required=True, validate=(required))
    location = fields.Dict(required=True, validate=(required))
