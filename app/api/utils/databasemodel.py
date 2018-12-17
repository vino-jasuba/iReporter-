from psycopg2.extras import RealDictCursor
from flask import g
from .model import AbstractModel
from db.db_config import connect_db
from db.tables import create_tables, drop_tables
import settings


class ModelNotFound(Exception):
    pass


class DatabaseModel(AbstractModel):
    table = ''

    def __init__(self):
        self.conn = self.get_db_connection()
        self.curr = self.conn.cursor(cursor_factory=RealDictCursor)

    def all(self):
        query = "SELECT * FROM {}".format(self.table)
        self.curr.execute(query)
        results = self.curr.fetchall()

        return results

    def get_db_connection(self):
        if not hasattr(g, 'conn'):
            g.conn = connect_db()
            return g.conn

        return g.conn

    def find_or_fail(self, id):
        """Find a record with a given id or fail"""
        record = self.find(id)

        if not record:
            raise ModelNotFound()

        return record

    def __update_string(self, data):
        string = ""

        for key, value in data.items():
            string += "{}".format(key) + " = " + "%s".format(value) + ","

        return string[:-1]

    def update(self, id, data):
        query = "UPDATE {} SET {} WHERE id = '{}' RETURNING {}.*".format(
            self.table, self.__update_string(data), id, self.table
        )

        self.curr.execute(query, tuple(data.values()))
        self.conn.commit()
        return self.curr.fetchone()

    def find(self, id):
        query = "SELECT * FROM {} WHERE id = %s".format(self.table, id)
        self.curr.execute(query, (id,))

        results = self.curr.fetchone()

        if results:
            return results

        return None

    def delete(self, id):
        query = "DELETE FROM {} WHERE id = %s".format(self.table)
        self.curr.execute(query, (id,))
        self.conn.commit()
        return True

    def where(self, key, value):
        query = "SELECT * FROM {} WHERE {} = %s".format(
            self.table, key)

        self.curr.execute(query, (value,))
        return self.curr.fetchall()

    def exists(self, key, value):
        query = "SELECT COUNT (*) FROM {} WHERE {} = %s".format(
            self.table, key)
        self.curr.execute(query, (value,))
        
        result = self.curr.fetchone()

        return result['count']

    def clear(self):
        query = "DELETE FROM {}".format(self.table)
        self.curr.execute(query)
        self.conn.commit()
