import argparse
import os
import settings
from db.db_config import connect_db
from db.tables import create_tables, drop_tables, truncate, seed


def migrate(connection):
    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Database management tool for iReporter')

    parser.add_argument(
        '-a', '--action', metavar='[migrate|truncate|seed]', help='Database action',
        choices={'migrate', 'truncate', 'seed'}, const='migrate', nargs='?')

    args = parser.parse_args()

    conn = connect_db()

    if args.action == 'migrate':
        migrate(conn)
    elif args.action == 'truncate':
        truncate(conn)
    elif args.action == 'seed':
        seed(conn)
    else:
        pass

    conn.close()
