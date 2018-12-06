from app.api.utils.databasemodel import DatabaseModel


class UserModel(DatabaseModel):

    table = 'users'

    def all(self):
        query = "SELECT * FROM {}".format(self.table)
        self.curr.execute(query)
        results = self.curr.fetchall()

        self.collection = results

        return self.__pretifycollection()

    def save(self, data):
        query = "INSERT INTO {} (firstname, lastname, username, email, password) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
            self.table, data['firstname'],
            data['lastname'], data['username'], data['email'],
            data['password'])

        cur = self.conn.cursor()

        cur.execute(query)

        self.conn.commit()

    def find(self, id):
        query = "SELECT * FROM {} WHERE id = {}".format(self.table, id)
        self.curr.execute(query)

        results = self.curr.fetchone()
        if results:
            return self.__pretify(results)

        return None

    def __update_string(self, data):
        string = ""

        for key, value in data.items():
            string += "{}".format(key) + " = " + "'{}'".format(value) + ","

        return string[:-1]

    def update(self, id, data):
        query = "UPDATE {} SET {} WHERE id = '{}'".format(
            self.table, self.__update_string(data), id)

        self.curr.execute(query)
        self.conn.commit()

        return {}

    def delete(self, id):
        query = "DELETE FROM {} WHERE id = {}".format(self.table, id)
        self.curr.execute(query)
        self.conn.commit()
        return True

    def where(self, key, value):
        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)
        self.curr.execute(query)
        self.collection = self.curr.fetchall()

        return self.__pretifycollection()

    def exists(self, key, value):
        query = "SELECT COUNT (*) FROM {} WHERE {} = {}".format(self.table, key, value)
        self.curr.execute(query)
        result = self.curr.fetchone()

        return result[0]

    def __pretifycollection(self):

        return [self.__pretify(data) for data in self.collection]

    def __pretify(self, data):

        print(data)
        return {
            'id': data[0],
            'firstname': data[1],
            'lastname': data[2],
            'username': data[3],
            'othernames': data[4],
            'email': data[5],
            'registered': data[7].strftime('%c'),
            'role': data[8]
        }


if __name__ == "__main__":
    pass
