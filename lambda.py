import json
import message
import database
import utils
from functools import reduce

def handler(event, context):
    request_body = json.loads(event['body']) # Extract the Body from the call
    chat_id = json.dumps(request_body['message']['chat']['id']) # Extract the chat id from message
    command = json.dumps(request_body['message']['text']).strip('"') # Extract the text from the message

    database.update()
  
    if command == '/start':
        message.send_start(chat_id)
        
    elif command == '/help':
        message.send_help(chat_id)
    
    elif command == '/bookings':
        bookings = database.get_bookings()
        
        if len(bookings) == 0:
            message.send_no_bookings(chat_id)
        else:
            initial_str = "Here are the current bookings:\n\n"
            final_str = reduce(lambda acc, next: acc + "\n" + str(next), bookings, initial_str)
            message.send(chat_id, final_str)

    elif command == '/book':
        msg_str = "Choose the day of your booking:"
        keyboard_markup = utils.generate_keyboard_markup()
        message.send(chat_id, msg_str, keyboard_markup)
            
    else:
        message.send_unknown_command(chat_id)
    
    return {
        'statusCode': 200
    }