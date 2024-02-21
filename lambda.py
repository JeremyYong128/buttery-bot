import json
import utils
import database
from models.Message import Message
from functools import reduce

def handler(event, context):
    request_body = json.loads(event['body']) # Extract the Body from the call
    chat_id = json.dumps(request_body['message']['chat']['id']) # Extract the chat id from message
    command = json.dumps(request_body['message']['text']).strip('"') # Extract the text from the message

    database.update()
  
    if command == '/start':
        Message().with_chat_id(chat_id).with_text(utils.WELCOME_MESSAGE + "\n\n" + utils.HELP_MESSAGE).send()
        
    elif command == '/help':
        Message().with_chat_id(chat_id).with_text(utils.HELP_MESSAGE + "\n\n" + utils.CONTACT_MESSAGE).send()
    
    elif command == '/bookings':
        bookings = database.get_bookings()
        
        if len(bookings) == 0:
            Message().with_chat_id(chat_id).with_text(utils.NO_BOOKINGS_MESSAGE).send()
        else:
            initial_str = "Here are the current bookings:\n\n"
            final_str = reduce(lambda acc, next: acc + "\n" + str(next), bookings, initial_str)
            Message().with_chat_id(chat_id).with_text(final_str).send()

    # elif command == '/book':
            
    else:
        Message().with_chat_id(chat_id).with_text(utils.UNKNOWN_COMMAND_MESSAGE).send()
    
    return {
        'statusCode': 200
    }