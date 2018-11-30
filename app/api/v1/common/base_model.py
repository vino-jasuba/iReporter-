
from werkzeug.exceptions import BadRequest

class Model():
    def __init__(self, collection_list):
        self.collection = collection_list

    def all(self):
        return self.collection

    def save(self, data):

        data['id'] = self.__generate_user_id()

        self.collection.append(data)

    def find(self, id):

        for item in self.collection:
            if item['id'] == id:
                return item

        return None

    def update(self, model, data):

        for key, value in data.items():
            if key in model:
                model.update({key: value})
            else:
                raise BadRequest('update key {} with value {} failed! Key not found in base model'.format(key, value))

    def delete(self, id):
        item = self.find(id)

        if not item:
            return None
        else:
            self.collection.remove(item)
            return item

    def where(self, key, value):

        self.query = []

        for item in self.collection:
            if item[key] == value:
                self.query.append(item)

        return self

    def exists(self, key, value):

        return len(self.where(key, value).get()) > 0

    def get(self):
        return self.query

    def __generate_user_id(self):

        if len(self.collection):
            return self.collection[-1]['id'] + 1
        else:
            return 1
