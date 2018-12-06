from db_config import connect_db
import psycopg2
import datetime

create_table_queries = [
    """CREATE TABLE IF NOT EXISTS roles (
        id SERIAL NOT NULL PRIMARY KEY,
        role_name VARCHAR(48) NOT NULL,
        role_slug VARCHAR(48) NOT NULL
    )
    """,
    """CREATE TABLE IF NOT EXISTS users (
        id SERIAL NOT NULL PRIMARY KEY,
        firstname VARCHAR(191) NOT NULL,
        lastname VARCHAR(191) NOT NULL,
        username VARCHAR(191) NOT NULL,
        othernames VARCHAR(191) NULL,
        email VARCHAR(191) NOT NULL UNIQUE,
        password VARCHAR(191) NOT NULL,
        registered TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
        role INTEGER NOT NULL,
        FOREIGN KEY (role) REFERENCES roles(id)
        )
    """,
    """CREATE TABLE IF NOT EXISTS incidents (
        id SERIAL PRIMARY KEY,
        type VARCHAR(48) NOT NULL,
        title VARCHAR(191) NOT NULL,
        description TEXT NOT NULL,
        latitude float NOT NULL,
        longitude float NOT NULL, 
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
        created_by INTEGER NOT NULL,
        FOREIGN KEY (created_by) REFERENCES users(id)
    )
    """
]


tables = [
    "roles",
    "users",
    "incidents"
]


def drop_tables(connection):
    cur = connection.cursor()

    for table in tables:
        cur.execute("DROP TABLE IF EXISTS {} CASCADE".format(table))

    connection.commit()


def create_tables(connection):

    cur = connection.cursor()

    for query in create_table_queries:
        cur.execute(query)

    cur.execute("INSERT INTO roles (role_name, role_slug) VALUES ('{}', '{}')".format(
        'User', 'user'))
    cur.execute("INSERT INTO users (firstname, lastname, username, email, password, registered, role)\
    VALUES ('Vincent', 'Odhiambo', 'vino', 'admin@app.com', 'password', '{}', 1)".format(datetime.datetime.now().strftime('%c')))

    connection.commit()


if __name__ == "__main__":
    conn = connect_db()
    drop_tables(conn)
    create_tables(conn)
    conn.close()
    