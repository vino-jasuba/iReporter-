from app.api.utils.databasemodel import DatabaseModel


class IncidentModel(DatabaseModel):
    table = 'incidents'
    statuses = ['under_investigation', 'rejected',
                'resolved', 'draft', 'pending']

    def __init__(self):
        super().__init__()

    def save(self, data):
        type_ = data['incident_type']
        title_ = data['title']
        description_ = data['description']
        location_ = data['location']
        created_by = data['created_by']
        query = "INSERT INTO {} (incident_type, title, description, location, created_by) VALUES" \
                " (%s, %s, %s, %s, %s) RETURNING {}.*".format(self.table, self.table)

        self.curr.execute(query, (type_, title_, description_, location_, created_by))
        self.conn.commit()
        return self.curr.fetchone()

    def load_media(self, incident_id):

        self.curr.execute("SELECT * FROM media where incident_id = %s", (incident_id,))

        return self.curr.fetchall()