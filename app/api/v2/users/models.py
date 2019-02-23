from app.api.utils.databasemodel import DatabaseModel


class UserModel(DatabaseModel):
    table = 'users'

    def save(self, data):
        firstname_ = data['firstname']
        lastname_ = data['lastname']
        username_ = data['username']
        email_ = data['email']
        password_ = data['password']

        query = "INSERT INTO {} (firstname, lastname, username, email, password)" \
                " VALUES (%s, %s, %s, %s, %s) RETURNING {}.*".format(self.table, self.table)

        self.curr.execute(query, (firstname_, lastname_,
                                  username_, email_, password_))
        self.conn.commit()
        return self.curr.fetchone()


class ExpiredTokenModel(DatabaseModel):
    table = 'expired_tokens'

    def save(self, data):
        query = "INSERT INTO {} (jti) VALUES (%s)".format(self.table)
        self.curr.execute(query, (data['jti'],))
        self.conn.commit()
        return {}


if __name__ == "__main__":
    pass
