import os
import requests
from utils import format_booking_date

HELP_MESSAGE = "- /book: get started with booking the buttery.\n- /bookings: view all approved bookings for the next 7 days.\n- /delete: delete your booking.\n- /help: view all commands.\n- /mybooking: view your current booking."
PREVIOUS_BOOKING_MESSAGE = "You already have a previous booking. To add a new booking, cancel the previous one first."
REQUEST_STRING = 'https://api.telegram.org/bot' + os.environ.get('TOKEN') + '/'
ADMIN_CHAT_ID = "-4158095181"

def send(chat_id, text, markup=None):
    request_string = REQUEST_STRING + 'sendMessage?chat_id=' + chat_id + '&text=' + text
    if markup:
        request_string += '&reply_markup=' + markup
    requests.get(request_string)

def send_start(chat_id):
    send(chat_id, "Welcome to Saga Buttery Bot!" + "\n\n" + HELP_MESSAGE)

def send_help(chat_id):
    send(chat_id, HELP_MESSAGE + "\n\n" + "For more assistance, contact @carinateh, @jemmacheah, @jeremyyong128, @owenyeoo, or @ymirmeddeb.")

def send_unknown_command(chat_id):
    send(chat_id, "Unknown command. Type /help for a list of commands.")

def send_set_booking_date(chat_id, date):
    send(chat_id, "The date of your booking has been set to " + format_booking_date(date) + ".\n\n" +
         "Enter the time of your booking in 24h format (HH:MM or HHMM). Note that bookings can only be made on the hour or half hour.")
    
def send_set_booking_time(chat_id, hour, min):
    send(chat_id, "The time of your booking has been set to " + str(hour) + ":" + str(min) + ".")

def send_to_admin(text):
    send(ADMIN_CHAT_ID, text)