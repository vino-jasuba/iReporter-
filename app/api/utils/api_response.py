class ApiResponse:
    """Represents generic API Response class"""

    __status_code = 200

    def setStatusCode(self, status_code):
        """Set status code for response"""
        self.__status_code = status_code

        return self

    def respondNotFound(self):
        """Return 404 Not found response"""
        return self.setStatusCode(404).respond({'message': 'resource not found'})

    def respondUnprocessibleEntity(self, data):
        """Return 422 Unprocessable entity response"""
        return self.setStatusCode(422).respond(data)

    def respondUnauthorized(self, message=None):
        """Return 401 Unauthorized response"""
        if message:
            return self.setStatusCode(401).respond({'message': message})

        return self.setStatusCode(401).respond({'message': 'Unauthorized'})

    def respondEntityCreated(self, data):
        return self.setStatusCode(201).respond(data)

    def respond(self, data):
        """Return 200 Ok response"""
        data.update({'status': self.getStatusCode()})

        return data, self.getStatusCode()

    def getStatusCode(self):
        return self.__status_code
