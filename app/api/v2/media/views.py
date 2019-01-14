import os
from minio import Minio
from minio.error import ResponseError
from werkzeug.utils import secure_filename
from flask_restful import request, Resource
from app.api.v2.roles.roles import is_admin
from app.api.v2.media.models import MediaModel
from app.api.v2.media.schema import MediaSchema
from app.api.utils.api_response import ApiResponse
from flask_jwt_extended import jwt_required, get_jwt_identity


class MediaList(Resource, ApiResponse):

    def __init__(self):

        self.db = MediaModel()

    def post(self):

        if not os.path.isdir('uploads'):
            os.mkdir('uploads')

        file = request.files['file']
        new_file_name = secure_filename(file.filename)
        file.save(os.path.join('uploads/', new_file_name))

        minioClient = Minio(
            os.getenv('STORAGE_URL'),
            access_key=os.getenv('MINIO_ACCESS_KEY'),
            secret_key=os.getenv('MINIO_SECRET_KEY'),
            secure=True
        )

        try:
            result = minioClient.fput_object(
                os.getenv('MINIO_BUCKET'),
                new_file_name,
                os.path.join('uploads/', new_file_name),
            )

            self.db.save({
                'type': file.filename.rsplit('.', 1)[1].lower(),
                'handle': ','.join(new_file_name),
                'created_by': 1
            })
        except Exception as e:
            print(e)

        return self.respondEntityCreated({
            'message': 'Image upload succeeded'
        })

    def get(self):

        # if is admin return all
        # else return for this user
        return self.respond({
            'data': MediaSchema(many=True).dump(self.db.all())[0]
        })


class Media(Resource, ApiResponse):

    def __init__(self):
        self.db = MediaModel()

    def get(self, resource_id):

        data = self.db.find_or_fail(resource_id)

        return MediaSchema().dump(data)[0]
