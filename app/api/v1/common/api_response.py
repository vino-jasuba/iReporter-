
class ApiResponse():

    def respondNotFound(self):
        return {'message': 'resource not found', 'status': 404}, 404
