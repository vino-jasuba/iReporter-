from abc import ABC, abstractmethod

class AbstractModel(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def save(self, data):
        pass

    @abstractmethod
    def find(self, id):
        pass

    @abstractmethod
    def update(self, id, data):
        pass

    @abstractmethod
    def delete(self, id):
        pass

    @abstractmethod
    def exists(self, key, value):
        pass
