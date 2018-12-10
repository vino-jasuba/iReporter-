import psycopg2
import os
import sys
import logging

DSN = ""


def connect_db():

    database = os.getenv('DB_DATABASE')
    user = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')

    DSN = "dbname='{}' user='{}' password='{}' host='{}'".format(
        database, user, password, host)

    logger = logging.getLogger('database')

    try:
        conn = psycopg2.connect(DSN)
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)

    return conn
