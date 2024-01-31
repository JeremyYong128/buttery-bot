import json
import os
import requests
import psycopg2
import urllib.parse as up
from psycopg2 import Error


BOT_TOKEN = os.environ.get('TOKEN')
HELP_MESSAGE = "- Type /bookings to view all bookings for the next 7 days.\n- Type /book to get started with booking the buttery."

def handler(event, context):
    print(event)
    request_body = json.loads(event['body']) # Extract the Body from the call
    BOT_CHAT_ID = json.dumps(request_body['message']['chat']['id']) # Extract the chat id from message
    command = json.dumps(request_body['message']['text']).strip('"') # Extract the text from the message

    command = command[1:] # Valid input command is /start or /help. however stripping the '/' here as it was having some conflict in execution.
    
    if command == 'start':
        send_message(BOT_TOKEN, BOT_CHAT_ID, "Welcome to ButteryBot!\n\n" + HELP_MESSAGE)
        
    elif command == 'help':
        send_message(BOT_TOKEN, BOT_CHAT_ID, HELP_MESSAGE)

    # elif command == 'nigga':
    #     db_connect()

    # elif command == 'bookings':
    #     conn = db_connect()

    # elif command == 'book':
    
    else:
        send_message(BOT_TOKEN, BOT_CHAT_ID, "I'm sorry, I didn't understand that command. Please try again.")
    
    return {
        'statusCode': 200
    }

def db_connect():
    try:
        up.uses_netloc.append("postgres")
        url = up.urlparse(os.environ["DATABASE_URL"])
        conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
        return conn
    except Error as e:
        return False
    
def send_message(bot_token, chat_id, message):
    requests.get('https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '\&parse_mode=HTML&text=' + message)