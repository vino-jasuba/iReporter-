from .model import AbstractModel
from db.db_config import connect_db
from db.tables import create_tables
import settings

conn = connect_db()

class DatabaseModel(AbstractModel):

    def __init__(self):
        
        self.conn = conn
        self.curr = conn.cursor()

