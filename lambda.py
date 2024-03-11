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
            initial_str = "Here are the current bookings:\n\n"
            final_str = reduce(lambda acc, next: acc + "\n" + str(next), bookings, initial_str)
            message.send(chat_id, final_str)

    elif command == '/book':
        if user_status == "has previous booking":
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
                else:
                    message.send(chat_id, "The time provided is not valid. The start time of bookings has to be from 8am to 11:30pm.")
        else:
            message.send(chat_id, "Invalid time format, make sure it follows the 24h format and is on the hour/half hour (e.g. 23:00, 1430).")

    # elif user_status == "setting duration":
        


                

    
    else:
        message.send_unknown_command(chat_id)


def handle_callback(update):
    chat_id = json.dumps(update['callback_query']['message']['chat']['id'])
    handle = json.dumps(update['callback_query']['from']['username']).strip('"')
    user_status = database.get_user_status(handle)
    
    if user_status == "has previous booking":
        message.send(chat_id, message.PREVIOUS_BOOKING_MESSAGE)
    else:
        date = datetime.datetime.today() + datetime.timedelta(days=int(json.dumps(update['callback_query']['data']).strip('"')))
        database.update_booking_date(handle, date, user_status)
        message.send_set_booking_date(chat_id, date)