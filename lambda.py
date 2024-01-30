import json
import os
import requests
import psycopg2
import urllib.parse as up
from psycopg2 import Error

help_message = "- Type /bookings to view all bookings for the next 7 days.\n- Type /book to get started with booking the buttery."

def handler(event, context):
    request_body = json.loads(event['body']) # Extract the Body from the call
    chat_id = json.dumps(request_body['message']['chat']['id']) # Extract the chat id from message
    command = json.dumps(request_body['message']['text']).strip('"') # Extract the text from the message

    BOT_TOKEN = os.environ.get('TOKEN')
    BOT_CHAT_ID = chat_id # Updating the Bot Chat Id to be dynamic instead of static one earlier
    command = command[1:] # Valid input command is /start or /help. however stripping the '/' here as it was having some conflict in execution.
    
    if command == 'start':
        message = "Welcome to ButteryBot!\n\n" + help_message
        
    elif command == 'help':
        message = help_message

    # elif command == 'nigga':
    #     db_connect()

    # elif command == 'bookings':
    #     conn = db_connect()

    #     if not conn:
    #         send_error_message("Sorry, there was an error ")

    # elif command == 'book':
    
    else:
        message = "I'm sorry, I didn't understand that command. Please try again."

    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + BOT_CHAT_ID + '\&parse_mode=HTML&text=' + message
    response = requests.get(send_text)
    
    return {
        'statusCode': 200,
        'method': "sendMessage",
        'text': "This is from the return value"
    }

def db_connect():
    try:
        up.uses_netloc.append("postgres")
        url = up.urlparse(os.environ["DATABASE_URL"])
        conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
        return conn
    except Error as e:
        return False