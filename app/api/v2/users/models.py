from app.api.utils.databasemodel import DatabaseModel


class UserModel(DatabaseModel):
    table = 'users'

    def save(self, data):
        query = "INSERT INTO {} (firstname, lastname, username, email, password)" \
                " VALUES ('{}', '{}', '{}', '{}', '{}') RETURNING {}.*".format(
                    self.table, data['firstname'],
                    data['lastname'], data['username'], data['email'],
                    data['password'], self.table)

        self.curr.execute(query)
        self.conn.commit()
        return self.curr.fetchone()


if __name__ == "__main__":
    pass
