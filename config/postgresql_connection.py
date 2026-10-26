import psycopg2

def create_postgresql_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="ecommercetarget",
        user="postgres",
        password="3021"
    )

    return conn


