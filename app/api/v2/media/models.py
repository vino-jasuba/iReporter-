from app.api.utils.databasemodel import DatabaseModel


class MediaModel(DatabaseModel):
    table = 'media'
    default_search_key = 'handle'

    def save(self, data):
        _type = data['type']
        handle = data['handle']
        object_id = data['object_id']
        incident_id = data['incident_id']
        created_by = data['created_by']
        query = "INSERT INTO {} (type, handle, object_id, incident_id, created_by) VALUES" \
                " (%s, %s, %s, %s, %s) RETURNING {}.*".format(self.table, self.table)

        self.curr.execute(
            query, (_type, handle, object_id, int(incident_id), created_by))
        self.conn.commit()
        return self.curr.fetchone()
