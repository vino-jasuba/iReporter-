
from werkzeug.exceptions import BadRequest


class Model():
    """Represents the base model that defines connection with data store
    classes that communicate with the data store should extend this class
    to get access to methods for doing common data operations.
    """

    def __init__(self, collection_list):
        """
        :param collection_list: a list which will serve as the model's data store.
        """

        self.collection = collection_list

    def all(self):
        """Return all items in data store."""

        return self.collection

    def save(self, data):
        """Insert given data into the data store."""

        data['id'] = self.__generate_user_id()

        self.collection.append(data)

    def find(self, id):
        """Returns data item with id given, 
           if data is not found, return None.
        """

        for item in self.collection:
            if item['id'] == id:
                return item

        return None

    def update(self, model, data):
        """Updates given model with the given data.
           it first checks if the keys in the given data exist on the model 
           if they don't it raises a BadRequest exception.
        """

        for key, value in data.items():
            if key in model:
                model.update({key: value})
            else:
                raise BadRequest(
                    'update key {} with value {} failed! Key not found in base model'.format(key, value))

    def delete(self, id):
        """Deletes record with given id."""
        item = self.find(id)

        if not item:
            return None
        else:
            self.collection.remove(item)
            return item

    def clear(self):
        """Delete all records from data store."""
        self.collection.clear()

    def where(self, key, value):
        """
        :param key: key to check 
        :param value: the value to search for in given key

        Returns a new list containing the subset of the data found.
        """
        
        self.query = []

        for item in self.collection:
            if item[key] == value:
                self.query.append(item)

        return self

    def exists(self, key, value):
        """
        :param key: key to check
        :param value: value to search for in given key

        Returns boolean, True if it finds at least one record. False otherwise.
        """
        
        return len(self.where(key, value).get()) > 0

    def get(self):
        """Fetch results from query list."""

        return self.query

    def __generate_user_id(self):
        # generates a user id by incrementing the latest id 
        # on the data store. If no records, returns 1

        if len(self.collection):
            return self.collection[-1]['id'] + 1
        else:
            return 1
