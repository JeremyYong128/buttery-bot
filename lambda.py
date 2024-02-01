import json
import os
import requests
import messages
import database


BOT_TOKEN = os.environ.get('TOKEN')

def handler(event, context):
    print(event)
    request_body = json.loads(event['body']) # Extract the Body from the call
    BOT_CHAT_ID = json.dumps(request_body['message']['chat']['id']) # Extract the chat id from message
    command = json.dumps(request_body['message']['text']).strip('"') # Extract the text from the message
  
    if command == '/start':
        send_message(BOT_TOKEN, BOT_CHAT_ID, messages.WELCOME_MESSAGE + "\n\n" + messages.HELP_MESSAGE)
        
    elif command == '/help':
        send_message(BOT_TOKEN, BOT_CHAT_ID, messages.HELP_MESSAGE + "\n\n" + messages.CONTACT_MESSAGE)
    
    elif command == '/testdb':
        conn = database.get_connection()
        rows = database.query(conn)
        for row in rows:
            send_message(BOT_TOKEN, BOT_CHAT_ID, row)

    else:
        send_message(BOT_TOKEN, BOT_CHAT_ID, "I'm sorry, I didn't understand that. Please try again.")
    
    return {
        'statusCode': 200
    }
    
def send_message(bot_token, chat_id, message):
    requests.get('https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '\&parse_mode=HTML&text=' + message)