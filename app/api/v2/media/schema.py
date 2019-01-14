from marshmallow import fields, Schema, pre_dump
from minio import Minio
from minio.error import ResponseError
import os


minioClient = Minio(
    os.getenv('STORAGE_URL'),
    access_key=os.getenv('MINIO_ACCESS_KEY'),
    secret_key=os.getenv('MINIO_SECRET_KEY')
)


class MediaSchema(Schema):

    handle = fields.Str(required=True)
    type = fields.Str(required=True)

    @pre_dump
    def load_image(self, data):
        try:
            response = minioClient.presigned_get_object(
                os.getenv('MINIO_BUCKET'),
                data['handle'],
            )

            return data.update({
                'handle': response
            })
        except ResponseError as e:
            print(e)
            return data
