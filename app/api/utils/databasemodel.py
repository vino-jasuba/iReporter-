from psycopg2.extras import RealDictCursor
from flask import g
from .model import AbstractModel
from db.db_config import connect_db
from db.tables import create_tables, drop_tables
import settings



class DatabaseModel(AbstractModel):

    def __init__(self):

        self.conn = self.get_db_connection()
        self.curr = self.conn.cursor(cursor_factory=RealDictCursor)
        pass

        
    def get_db_connection(self):
        
        if not hasattr(g, 'psql'):
            g.conn = connect_db()
            return g.conn
        
        return g.conn
