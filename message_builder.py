import requests
import os

BOT_TOKEN = os.environ.get('TOKEN')

class Message:
    def __init__(self):
        self.chat_id = None
        self.text = None

    def with_chat_id(self, chat_id):
        self.chat_id = chat_id
        return self

    def with_text(self, text):
        self.text = text
        return self

    def send(self):
        if (self.chat_id is None) or (self.text is None):
            return False
        
        requests.get('https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + self.chat_id + '\&parse_mode=HTML&text=' + self.text)
        return True