import json
import message
import database
import utils
import datetime
from functools import reduce
from models.Booking import Booking

def handler(event, context):
    update = json.loads(event['body'])
    database.update()

    if 'message' in update:
        handle_message(update)

    if 'callback_query' in update:
        handle_callback(update)
    
    return {
        'statusCode': 200
    }

def handle_message(update):
    chat_id = json.dumps(update['message']['chat']['id'])
    command = json.dumps(update['message']['text']).strip('"')
    handle = json.dumps(update['message']['from']['username']).strip('"')
    user_status = database.get_user_status(handle)
  
    if command == '/start':
        message.send_start(chat_id)
        
    elif command == '/help':
        message.send_help(chat_id)
    
    elif command == '/bookings':
        bookings = database.get_approved_bookings()
        
        if len(bookings) == 0:
            message.send(chat_id, "There are no bookings.")
        else:
            initial_str = "Here are all the current bookings:\n\n"
            final_str = reduce(lambda acc, next: acc + "\n" + str(next), bookings, initial_str)
            message.send(chat_id, final_str)
    
    elif command == '/mybooking':
        booking = database.get_user_booking(handle)

        if booking is None:
            message.send(chat_id, "You have no bookings.")
        elif booking.get_status() == "approved":
            message.send(chat_id, "You have one approved booking:\n\n" + str(booking))
        elif booking.get_status() == "unapproved":
            message.send(chat_id, "You have one unapproved booking:\n\n" + str(booking))
        else:
            message.send(chat_id, "You have one booking in progress:\n\n" + str(booking))

    elif command == '/delete':
        booking = database.get_user_booking(handle)

        if booking is None:
            message.send(chat_id, "You have no bookings. To create a booking, enter /book")
        elif booking.get_status() == "approved":
            message.send(chat_id, "You have one approved booking:\n\n" + str(booking) + "\n\nDo you want to delete this booking?", utils.yes_no_keyboard_markup())
        elif booking.get_status() == "unapproved":
            message.send(chat_id, "You have one unapproved booking:\n\n" + str(booking) + "\n\nDo you want to delete this booking?", utils.yes_no_keyboard_markup())
        else:
            message.send(chat_id, "You have one booking in progress:\n\n" + str(booking) + "\n\nDo you want to delete this booking?", utils.yes_no_keyboard_markup())

    elif command == '/book':
        if user_status == "approved" or user_status == "unapproved":
            message.send(chat_id, message.PREVIOUS_BOOKING_MESSAGE)
        else:
            msg_str = "Choose the day of your booking:"
            keyboard_markup = utils.generate_dates_keyboard_markup()
            message.send(chat_id, msg_str, keyboard_markup)

    elif user_status == "setting time":
        if utils.is_valid_time_format(command):
                hour, min = utils.parse_time_string(command)

                if Booking.is_valid_start_time(hour):
                    database.update_booking_time(handle, hour, min)
                    message.send(chat_id, "The time of your booking has been set to " + str(hour) + ":" + (str(min) if min else "00") + ".\n\n" + 
                                 "Enter the duration of your booking. Note that bookings can be a maximum of 2h long, and must be in intervals of 0.5h.")
                else:
                    message.send(chat_id, "Invalid time provided. The start time of bookings has to be from 8am to 11:30pm (0800 - 2330).")
        else:
            message.send(chat_id, "Invalid time format. Make sure it follows the 24h format and is on the hour/half hour (e.g. 23:00, 1430).")

    elif user_status == "setting duration":
        try:
            duration = float(command)
            if duration not in Booking.acceptable_durations:
                message.send(chat_id, "Invalid duration provided. Duration must be a minimum of 0.5h and a maximum of 2h, and in intervals of 0.5h (i.e. values like 0.75 will not be accepted)")
            else:
                booking = database.get_user_booking(handle)
                end_time = Booking.calculate_end_time(booking.start_time, duration)
                if Booking.is_valid_end_time(end_time):
                    database.update_booking_duration(handle, duration)
                    message.send(chat_id, "The duration of your booking has been set to " + str(duration) + " hours.")
                    booking = database.get_user_booking(handle)
                    message.send(chat_id, "Your booking has been made!\n\n" + str(booking))
                else:
                    message.send(chat_id, "Invalid duration provided. Bookings must end by 12am.")
                
        except ValueError:
            message.send(chat_id, "Invalid duration format. Make sure it is a valid duration (e.g. 0.5, 1).")
    
    else:
        message.send_unknown_command(chat_id)


def handle_callback(update):
    chat_id = json.dumps(update['callback_query']['message']['chat']['id'])
    handle = json.dumps(update['callback_query']['from']['username']).strip('"')
    user_status = database.get_user_status(handle)
    data = json.dumps(update['callback_query']['data']).strip('"')

    if data == "Yes" or data == "No":
        database.delete_booking(handle)
        message.send(chat_id, "Your booking has been deleted.")

    else:
        if user_status == "approved" or user_status == "unapproved":
            message.send(chat_id, message.PREVIOUS_BOOKING_MESSAGE)
        else:
            date = datetime.datetime.today() + datetime.timedelta(days=int(data))
            database.update_booking_date(handle, date, user_status)
            message.send_set_booking_date(chat_id, date)