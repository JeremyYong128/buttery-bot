import json
import message
import database
import utils
import datetime
from functools import reduce

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
  
    if command == '/start':
        message.send_start(chat_id)
        
    elif command == '/help':
        message.send_help(chat_id)
    
    elif command == '/bookings':
        bookings = database.get_approved_bookings()
        
        if len(bookings) == 0:
            message.send_no_bookings(chat_id)
        else:
            initial_str = "Here are the current bookings:\n\n"
            final_str = reduce(lambda acc, next: acc + "\n" + str(next), bookings, initial_str)
            message.send(chat_id, final_str)

    elif command == '/book':
        msg_str = "Choose the day of your booking:"
        keyboard_markup = utils.generate_dates_keyboard_markup()
        message.send(chat_id, msg_str, keyboard_markup)

    elif command == '/test':
        database.update_request_date('@bobbymcbobface', datetime.date.today())
            
    else:
        message.send_unknown_command(chat_id)

def handle_callback(update):
    chat_id = json.dumps(update['callback_query']['message']['chat']['id'])
    handle = json.dumps(update['callback_query']['from']['username']).strip('"')
    date = datetime.datetime.today() + datetime.timedelta(days=int(json.dumps(update['callback_query']['data']).strip('"')))
    outcome = database.update_request_date(handle, date)
    
    if outcome in ("insert", "update"):
        message.send_set_booking_date(chat_id, date)
    else:
        message.send(chat_id, "Fuck u")
