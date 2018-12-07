
class ApiResponse():
    """Represents generic API Response class"""
    
    def respondNotFound(self):
        """Return 404 Not found response"""

        return {'message': 'resource not found', 'status': 404}, 404

    def respondUnprocessibleEntity(self, message):
        """Return 422 Unprocessable entity response"""

        return {'message': 'error, ' + message, 'status': 422}, 422

    def respondUnauthorized(self, message=None):
        """Return 401 Unauthorized response"""
        status = 401 
        
        if message:
            return {'message': message, 'status': status}, status
        
        return {'message': 'Unauthorized', 'status': status}
