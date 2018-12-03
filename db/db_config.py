import psycopg2

dsn = "dbname=ireporter user=vino password=password host=localhost"

def connect_db():
    
    conn = psycopg2.connect(dsn)

    return conn 




if __name__ == "__main__":
    connect_db()