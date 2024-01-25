import json
import os
import requests
import psycopg2
import urllib.parse as up
from psycopg2 import Error

def handler(event, context):
    request_body = json.loads(event['body']) # EXtract the Body from the call
    request_msg = json.dumps(request_body['message'])#['chat']['id'] # Extract the message object which contrains chat id and text
    chat_id = json.dumps(request_body['message']['chat']['id']) # Extract the chat id from message
    command = json.dumps(request_body['message']['text']).strip('"') # Extract the text from the message

    # TODO implement
    BOT_TOKEN = os.environ.get('TOKEN')
    BOT_CHAT_ID = chat_id # Updating the Bot Chat Id to be dynamic instead of static one earlier
    command = command[1:] # Valid input command is /start or /help. however stripping the '/' here as it was having some conflict in execution.
    
    if command == 'start':
        message = "Welcome to ButteryBot! What would you like to do?"
        
    elif command == 'help':
        message = "Here are the available commands: /start, /help"

    elif command == 'nigga':
        try: 
            up.uses_netloc.append("postgres")
            url = up.urlparse(os.environ["DATABASE_URL"])
            conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
            message = "database connected nigga"
        except Error as e:
            message = f"Database error nigga: {e}"
    
    else:
        message = "I'm sorry, I didn't understand that command. Please try again."

    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + BOT_CHAT_ID + '\&parse_mode=HTML&text=' + message
    response = requests.get(send_text)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }