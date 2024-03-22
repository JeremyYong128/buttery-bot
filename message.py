import os
import requests

ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')
COMMAND_LIST = "- /book: get started with booking the buttery.\n- /bookings: view all approved bookings.\n- /delete: delete your booking.\n- /help: view all commands.\n- /mybooking: view your current booking."
GUIDELINES = "Booking guidelines:\n- The buttery opens at 8am and closes at 12am daily.\n- Bookings must be made a minimum of 24h and a maximum of 3 days in advance.\n- Your booking is only confirmed once an admin approves it. In the event that your request is rejected, our admins will contact you."
REQUEST_STRING = 'https://api.telegram.org/bot' + os.environ.get('TOKEN') + '/'

def send(chat_id, text, markup=None):
    request_string = REQUEST_STRING + 'sendMessage?chat_id=' + chat_id + '&text=' + text
    if markup:
        request_string += '&reply_markup=' + markup
    requests.get(request_string)   

def send_to_admin(text, markup=None):
    send(ADMIN_CHAT_ID, text, markup)