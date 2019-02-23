import psycopg2
import datetime
import os
from werkzeug.security import generate_password_hash
from termcolor import colored

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
        role INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (role) REFERENCES roles(id)
        )
    """,
    """CREATE TABLE IF NOT EXISTS incidents (
        id SERIAL PRIMARY KEY,
        incident_type VARCHAR(48) NOT NULL,
        title VARCHAR(191) NOT NULL,
        description TEXT NOT NULL,
        status VARCHAR(64) NOT NULL DEFAULT ('draft'),
        location VARCHAR(191) NOT NULL,
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
        created_by INTEGER NOT NULL,
        FOREIGN KEY (created_by) REFERENCES users(id)
    )
    """,
    """CREATE TABLE IF NOT EXISTS media (
        id SERIAL PRIMARY KEY,
        incident_id INTEGER NOT NULL,
        type VARCHAR(6) NOT NULL,
        handle VARCHAR(64) NOT NULL,
        object_id VARCHAR(64) NOT NULL,
        created_by INTEGER NOT NULL,
        FOREIGN KEY (created_by) REFERENCES users(id),
        FOREIGN KEY (incident_id) REFERENCES incidents(id)
    )
    """,
    """CREATE TABLE IF NOT EXISTS expired_tokens (
        id SERIAL PRIMARY KEY,
        jti VARCHAR(48) NOT NULL
    )
    """
]

tables = [
    "roles",
    "users",
    "incidents",
    "media",
    "expired_tokens"
]


def truncate(connection):
    cur = connection.cursor()
    cur.execute('TRUNCATE TABLE ' + ','.join(tables) +
                ' RESTART IDENTITY CASCADE')
    connection.commit()


def drop_tables(connection):
    cur = connection.cursor()

    for table in tables:
        cur.execute("DROP TABLE IF EXISTS {} CASCADE".format(table))
    connection.commit()


def create_tables(connection):
    cur = connection.cursor()

    for query in create_table_queries:
        cur.execute(query)
    connection.commit()


def seed(connection):
    cur = connection.cursor()
    cur.execute("INSERT INTO roles (role_name, role_slug) VALUES ('{}', '{}')".format(
        'User', 'user'))
    cur.execute("INSERT INTO roles (role_name, role_slug) VALUES ('{}', '{}')".format(
        'Admin', 'admin'))
    cur.execute("INSERT INTO users (firstname, lastname, username, email, password, role)\
        VALUES ('Vincent', 'Odhiambo', 'vino', 'admin@app.com', '{}', 2)".format(
        generate_password_hash(os.getenv('PASSWORD', 'PaSsw0rd'))))
    connection.commit()
