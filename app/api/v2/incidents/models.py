from app.api.utils.databasemodel import DatabaseModel


class IncidentModel(DatabaseModel):

    table = 'incidents'

    def __init__(self):
        super().__init__()

    def all(self):
        query = "SELECT * FROM {}".format(self.table)
        self.curr.execute(query)
        results = self.curr.fetchall()

        return results

    def save(self, data):
        query = "INSERT INTO {} (incident_type, title, description, latitude, longitude, created_by) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
            self.table, data['incident_type'],
            data['title'], data['description'], data['location']['lat'],
            data['location']['lng'], 1)

        cur = self.conn.cursor()

        cur.execute(query)

        self.conn.commit()

    def find(self, id):
        query = "SELECT * FROM {} WHERE id = {}".format(self.table, id)
        self.curr.execute(query)

        results = self.curr.fetchone()

        if results:
            return results

        return None

    def __update_string(self, data):
        string = ""

        for key, value in data.items():
            if key == 'location':
                string += "latitude = '{}'".format(value['lat']) + ","
                string += "longitude = '{}'".format(value['lng']) + ","
            else:
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

        return self.collection

    def exists(self, key, value):
        query = "SELECT COUNT (*) FROM {} WHERE {} = {}".format(self.table, key, value)
        self.curr.execute(query)
        result = self.curr.fetchone()

        return result[0]

    def clear(self):
        query = "DELETE FROM {}".format(self.table)
        self.curr.execute(query)
        self.conn.commit()

