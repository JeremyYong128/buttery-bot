import json
import os
import requests

def handler(event, context):
    request_body = json.loads(event['body']) # EXtract the Body from the call
    request_msg = json.dumps(request_body['message'])#['chat']['id'] # Extract the message object which contrains chat id and text
    chat_id = json.dumps(request_body['message']['chat']['id']) # Extract the chat id from message
    command = json.dumps(request_body['message']['text']).strip('"') # Extract the text from the message

    # TODO implement
    BOT_TOKEN = os.environ.get('TOKEN')
    BOT_CHAT_ID = os.environ.get('CHATID')
    BOT_CHAT_ID = chat_id # Updating the Bot Chat Id to be dynamic instead of static one earlier
    command = command[1:] # Valid input command is /start or /help. however stripping the '/' here as it was having some conflict in execution.
    
    if command == 'start':
        message = "Welcome to ButteryBot! What would you like to do?"
        # Create the custom keyboard
        keyboard = {
            'inline_keyboard': [
                [
                    {'text': 'Bookings', 'callback_data': 'option1'},
                    {'text': 'Check status', 'callback_data': 'option2'}
                ]
            ]
        }
        # Convert the keyboard to JSON
        reply_markup = json.dumps(keyboard)

        send_text = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={BOT_CHAT_ID}&parse_mode=HTML&text={message}&reply_markup={reply_markup}'
        response = requests.get(send_text)
        print(send_text)
        print(response)
        
    elif command == 'help':
        message = "Here are the available commands: /start, /help"
    elif command == 'nigga':
        message = "burh u cant say that lil nigga"
    else:
        message = "I'm sorry, I didn't understand that command. Please try again."

    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + BOT_CHAT_ID + '\&parse_mode=HTML&text=' + message
    response = requests.get(send_text)
    print(send_text) 
    print(response) 
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }