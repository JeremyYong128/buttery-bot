import requests
from utils import REQUEST_STRING

WELCOME_MESSAGE = "Welcome to Saga Buttery Bot!"
HELP_MESSAGE = "- Type /bookings to view all bookings for the next 7 days.\n- Type /book to get started with booking the buttery."
CONTACT_MESSAGE = "For more assistance, contact @carinateh, @jemmacheah, @jeremyyong128, @owenyeoo, or @ymirmeddeb."
UNKNOWN_COMMAND_MESSAGE = "Unknown command. Please ensure you have entered the correct command."
NO_BOOKINGS_MESSAGE = "There are no bookings."

def send(chat_id, text, markup=None):
    request_string = REQUEST_STRING + 'sendMessage?chat_id=' + chat_id + '&text=' + text
    if markup:
        request_string += '&reply_markup=' + markup
    requests.get(request_string)

def send_start(chat_id):
    send(chat_id, WELCOME_MESSAGE + "\n\n" + HELP_MESSAGE)

def send_help(chat_id):
    send(chat_id, HELP_MESSAGE + "\n\n" + CONTACT_MESSAGE)

def send_unknown_command(chat_id):
    send(chat_id, UNKNOWN_COMMAND_MESSAGE)

def send_no_bookings(chat_id):
    send(chat_id, NO_BOOKINGS_MESSAGE)

def send_booking_dates():
    return