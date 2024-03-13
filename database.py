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

def get_user_status(telegram_handle):
    if has_previous_booking(telegram_handle):
        return "has previous booking"
    elif is_setting_time(telegram_handle):
        return "setting time"
    elif is_setting_duration(telegram_handle):
        return "setting duration"
    else:
        return "no booking"

def has_previous_booking(telegram_handle):
    prev_booking = None
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("select * from bookings where telegram_handle = '" + telegram_handle + "' and duration is not null")
        prev_booking = cursor.fetchone()
    release_connection(conn)

    if prev_booking:
        return True
    return False

def get_user_booking(telegram_handle):
    booking = None
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("select * from bookings where telegram_handle = '" + telegram_handle + "'")
        booking = cursor.fetchone()
    return Booking(*booking) if booking else None
    
def is_setting_time(telegram_handle):
    halfway_booking = None
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("select * from bookings where telegram_handle = '" + telegram_handle + "' and start_time is null")
        halfway_booking = cursor.fetchone()
    release_connection(conn)

    if halfway_booking:
        return True
    return False

def is_setting_duration(telegram_handle):
    halfway_booking = None
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("select * from bookings where telegram_handle = '" + telegram_handle + "' and start_time is not null and duration is null")
        halfway_booking = cursor.fetchone()
    release_connection(conn)

    if halfway_booking:
        return True
    return False

def update_booking_date(telegram_handle, date, user_status):
    date_string = date.strftime("%Y-%m-%d")

    if user_status == "setting time" or user_status == "setting duration":
        conn = get_connection()
        with conn.cursor() as cursor:
            if user_status == "setting duration":
                cursor.execute("update bookings set start_time = NULL where telegram_handle = '" + telegram_handle + "'")
            cursor.execute("update bookings set date = '" + date_string + "' where telegram_handle = '" + telegram_handle + "'")
        release_connection(conn)
    else:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("insert into bookings (telegram_handle, date) values ('" + telegram_handle + "', '" + date_string + "')")
        release_connection(conn)

def update_booking_time(telegram_handle, hour, min):
    time_string = str(hour) + ":" + str(min) + ":00"
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("update bookings set start_time = '" + time_string + "' where telegram_handle = '" + telegram_handle + "'")
    release_connection(conn)

def update_booking_duration(telegram_handle, duration):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("update bookings set duration = " + str(duration) + " where telegram_handle = '" + telegram_handle + "'")
    release_connection(conn)