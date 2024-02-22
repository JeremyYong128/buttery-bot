import os
import urllib.parse as up
from psycopg2 import pool
from models.Booking import Booking
from datetime import date
from psycopg2.errors import UniqueViolation

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

    conn = connection_pool.getconn()
    conn.autocommit = True

    return conn

def release_connection(conn):
    connection_pool.putconn(conn)

def get_approved_bookings():
    bookings = None
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("select * from bookings where approved = true")
        bookings = cursor.fetchall()
    release_connection(conn)
    return list(map(lambda booking: Booking(*booking), bookings))

def update():
    date_string = date.today().strftime("%Y-%m-%d")
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("delete from bookings where date < '" + date_string + "'")
    release_connection(conn)

def update_request_date(telegram_handle, date):
    date_string = date.strftime("%Y-%m-%d")
    action = None
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("select * from bookings where telegram_handle = '" + telegram_handle + "'")
        booking_params = cursor.fetchone()

        if booking_params:
            current_booking = Booking(*booking_params)
            if current_booking.duration is None:
                cursor.execute("update bookings set date = '" + date_string + "' where telegram_handle = '" + telegram_handle + "'")
                action = "update"
            else:
                action = "none"
        else:
            cursor.execute("insert into bookings (telegram_handle, date) values ('" + telegram_handle + "', '" + date_string + "')")
            action = "insert"
            
    release_connection(conn)
    return action