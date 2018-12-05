import psycopg2

# TODO: export application configs to .env files
dsn = "dbname=ireporter user=vino password=password host=localhost"


def connect_db():

    try:
        conn = psycopg2.connect(
            "dbname='ireporter' user='vino' host='localhost' password='password'")
    except:
        print("something went wrong")

    return conn


if __name__ == "__main__":
    connect_db()
