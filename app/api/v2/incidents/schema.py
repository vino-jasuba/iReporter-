from marshmallow import Schema, fields, pre_dump, post_load
from app.api.utils.validator import not_empty, latitude, longitude, valid_type
import json
from .models import IncidentModel
from minio import Minio
from minio.error import ResponseError
import os

minioClient = Minio(
    os.getenv('STORAGE_URL'),
    access_key=os.getenv('MINIO_ACCESS_KEY'),
    secret_key=os.getenv('MINIO_SECRET_KEY')
)


class LocationSchema(Schema):
    lat = fields.Float(required=True, validate=(not_empty, latitude),
                       error_messages={'validator_failed': 'invalid latitude coordinate'})
    lng = fields.Float(required=True, validate=(not_empty, longitude),
                       error_messages={'validator_failed': 'invalid longitude coordinate'})
    city = fields.Str(required=True, validate=(not_empty),
                      error_messages={'validator_failed': 'you should provide a city'})

    @pre_dump
    def extract_location(self, data):
        data = json.loads(data)
        return data

    @post_load
    def stringify_location(self, data):
        data = json.dumps(data)
        return data


class IncidentSchema(Schema):
    """Represents the schema for incidents."""

    id = fields.Integer(required=False)
    incident_type = fields.Str(required=True, validate=(not_empty, valid_type))
    title = fields.Str(required=True, validate=(not_empty))
    description = fields.Str(required=True, validate=(not_empty))
    location = fields.Nested(LocationSchema, required=True)
    status = fields.Str(required=False, validate=(not_empty))
    created_at = fields.DateTime(required=False, format='%b, %d, %Y')
    images = fields.List(fields.String(), required=False)
    videos = fields.List(fields.String(), required=False)


class IncidentUpdateSchema(IncidentSchema):
    """Represents the schema for updating incidents"""
    incident_type = fields.Str(
        required=False, validate=(not_empty, valid_type))
    title = fields.Str(required=False, validate=(not_empty))
    description = fields.Str(required=False, validate=(not_empty))
    location = fields.Nested(LocationSchema, required=False,
                             error_messages={'validator_failed': 'invalid coordinate data found in request'})
    status = fields.Str(required=False, validate=(not_empty))

    @pre_dump
    def load_media(self, data):

        incident_media = IncidentModel().load_media(data['id'])
        image_mime_types = ['png', 'jpg', 'jpeg']
        video_mime_types = ['mp4', 'mkv']

        images = []
        videos = []

        for media in incident_media:
            try:
                response = minioClient.presigned_get_object(
                    os.getenv('MINIO_BUCKET'),
                    media['handle'],
                )

                if media['type'] in image_mime_types:
                    images.append(response)

                if media['type'] in video_mime_types:
                    videos.append(response)
            except ResponseError:
                pass

        return data.update({
            'images': images,
            'videos': videos
        })
