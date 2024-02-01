import os
import urllib.parse as up
from psycopg2 import pool
from models.Booking import Booking

connection_pool = None

def get_connection():
    global connection_pool
    if connection_pool is None:
        up.uses_netloc.append("postgres")
        url = up.urlparse(os.environ["DATABASE_URL"])

        connection_pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=5,
            dbname=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port)

    return connection_pool.getconn()

def release_connection(conn):
    connection_pool.putconn(conn)

def get_bookings():
    conn = get_connection()
    bookings = None
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM bookings")
        bookings = cursor.fetchall()
    release_connection(conn)
    return list(map(lambda booking: Booking(*booking), bookings))