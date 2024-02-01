import json
import messages
import database
import message_builder
from message_builder import Message

def handler(event, context):
    print(event)
    request_body = json.loads(event['body']) # Extract the Body from the call
    chat_id = json.dumps(request_body['message']['chat']['id']) # Extract the chat id from message
    command = json.dumps(request_body['message']['text']).strip('"') # Extract the text from the message
  
    if command == '/start':
        Message().with_chat_id(chat_id).with_text(messages.WELCOME_MESSAGE + "\n\n" + messages.HELP_MESSAGE).send()
        
    elif command == '/help':
        Message().with_chat_id(chat_id).with_text(messages.HELP_MESSAGE + "\n\n" + messages.CONTACT_MESSAGE).send()
    
    elif command == '/bookings':
        conn = database.get_connection()
        rows = database.query(conn)
        database.release_connection(conn)
        
        if len(rows) == 0:
            Message().with_chat_id(chat_id).with_text(messages.NO_BOOKINGS_MESSAGE).send()
        for row in rows:
            Message().with_chat_id(chat_id).with_text(str(row)).send()

    else:
        Message().with_chat_id(chat_id).with_text(messages.UNKNOWN_COMMAND_MESSAGE).send()
    
    return {
        'statusCode': 200
    }