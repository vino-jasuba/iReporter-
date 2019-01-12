from app.api.utils.databasemodel import DatabaseModel


def is_admin(user):
    return user['isAdmin']


class Role(DatabaseModel):
    table = 'roles'

    def save(self, data):
        query = "INSERT INTO {} (role_name, role_slug) VALUES ('{}', '{}')".format(self.table, data['role_name'],
                                                                                   data['role_slug'])
        self.curr.execute(query)
        self.conn.commit()

    def find(self, id):
        pass

    def update(self, id, data):
        pass

    def delete(self, id):
        pass

    def exists(self, key, value):
        pass

    def all(self):
        pass
