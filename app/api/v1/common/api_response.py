
class ApiResponse():

    def respondNotFound(self):
        return {'message': 'resource not found', 'status': 404}, 404

    def respondUnprocessibleEntity(self, message):
        return {'message': 'error, ' + message, 'status': 422}, 422