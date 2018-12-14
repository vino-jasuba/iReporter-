from app.api.utils.databasemodel import DatabaseModel
from werkzeug.exceptions import NotFound


class IncidentModel(DatabaseModel):
    table = 'incidents'
    statuses = ['under investigation', 'rejected',
                'resolved', 'draft', 'pending']

    def __init__(self):
        super().__init__()

    def save(self, data):
        query = "INSERT INTO {} (incident_type, title, description, latitude, longitude, created_by) VALUES" \
                " ('{}', '{}', '{}', '{}', '{}', '{}') RETURNING {}.*".format(self.table, data['incident_type'],
                                                                              data['title'], data['description'],
                                                                              data['location']['lat'],
                                                                              data['location']['lng'],
                                                                              data['created_by'],
                                                                              self.table)

        self.curr.execute(query)
        self.conn.commit()
        return self.curr.fetchone()
