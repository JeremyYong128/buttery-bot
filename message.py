import requests
from utils import REQUEST_STRING

WELCOME_MESSAGE = "Welcome to Saga Buttery Bot!"
HELP_MESSAGE = "- Type /bookings to view all bookings for the next 7 days.\n- Type /book to get started with booking the buttery."
CONTACT_MESSAGE = "For more assistance, contact @carinateh, @jemmacheah, @jeremyyong128, @owenyeoo, or @ymirmeddeb."
UNKNOWN_COMMAND_MESSAGE = "Unknown command. Please ensure you have entered the correct command."
NO_BOOKINGS_MESSAGE = "There are no bookings."

class Message:
    def with_chat_id(self, chat_id):
        self.chat_id = chat_id
        return self

    def with_text(self, text):
        self.text = text
        return self

    @staticmethod
    def send(chat_id, text, markup=None):
        request_string = REQUEST_STRING + 'sendMessage?chat_id=' + chat_id + '&text=' + text
        if markup:
            request_string += '&reply_markup=' + self.markup
        requests.get(request_string)

    @staticmethod
    def send_start(chat_id):
        Message.send(chat_id, WELCOME_MESSAGE + "\n\n" + HELP_MESSAGE)

    @staticmethod
    def send_help(chat_id):
        Message.send(chat_id, HELP_MESSAGE + "\n\n" + CONTACT_MESSAGE)
    
    @staticmethod
    def send_no_bookings(chat_id):
        Message.send(chat_id, NO_BOOKINGS_MESSAGE)
    
    @staticmethod
    def send_booking_dates(self):
        r