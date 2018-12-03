from db_config import connect_db
import psycopg2
import datetime

create_table_queries = [
    """CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY,
        firstname VARCHAR(191) NOT NULL,
        lastname VARCHAR(191) NOT NULL,
        username VARCHAR(191) NOT NULL UNIQUE ,
        othernames VARCHAR(191) NULL,
        email VARCHAR(191) NOT NULL UNIQUE,
        password VARCHAR(191) NOT NULL,
        registered TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
        )
        """,
    """CREATE TABLE IF NOT EXISTS incidents (
        id SERIAL PRIMARY KEY,
        type VARCHAR(20) NOT NULL,
        title VARCHAR(191) NOT NULL,
        description TEXT NOT NULL,
        latitude float NOT NULL,
        longitude float NOT NULL, 
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
        created_by INT NOT NULL,
        FOREIGN KEY (created_by) REFERENCES users(id)
    )"""
]


def create_tables():

    conn = connect_db()
    cur = conn.cursor()

    for query in create_table_queries:
        cur.execute(query)
        print("complete")

    cur.execute("INSERT INTO users (firstname, lastname, username, email, password, registered)\
    VALUES ('Vincent', 'Odhiambo', 'vino', 'admin@app.com', 'password', '{}')".format(datetime.datetime.now().strftime('%c')))


if __name__ == "__main__":
    create_tables()
