import datetime
import json
import re

def generate_dates_keyboard_markup():
    keyboard = [[ generate_keyboard_date_button(i)] for i in range(1, 4)]
    return json.dumps({
        "inline_keyboard": keyboard
    })

def generate_keyboard_date_button(days):
    date = datetime.date.today() + datetime.timedelta(days=days)
    day = str(date.day)
    month = str(date.month)
    year = str(date.year)
    date_string = format_booking_date(date)
    
    return {
        "text": date_string,
        "callback_data": " ".join(["BOOK", day, month, year])
    }

def confirm_keyboard_markup():
    return json.dumps({
        "inline_keyboard": [[{
            "text": "Confirm",
            "callback_data": "CONFIRM"
        }]]
    })

def admin_confirm_keyboard_markup(chat_id, handle, date: datetime.date, start_time: datetime.time, duration):
    return json.dumps({
        "inline_keyboard": [
            [{
                "text": "Approve",
                "callback_data": " ".join(["APPROVE", chat_id, handle, str(date.year), str(date.month), str(date.day), str(start_time.hour), str(start_time.minute), str(duration)])
            }], [{
                "text": "Reject",
                "callback_data": " ".join(["REJECT", chat_id, handle, str(date.year), str(date.month), str(date.day), str(start_time.hour), str(start_time.minute), str(duration)])
            }]]
    })

def format_booking_date(date):
    return date.strftime("%-d %b")

def is_valid_time_format(str):
    pattern = r'^\d{2}:?\d{2}$'
    if not re.match(pattern, str.strip()):
        return False
    
    digits = str.strip().replace(':', '')
    hour = int(digits[:2])
    min = int(digits[2:])
    
    if hour > 23 or (min not in (0, 30)):
        return False
    
    return True

def parse_time_string(str):
    str = str.strip().replace(':', '')
    hour = int(str[:2])
    min = int(str[2:])
    
    return hour, min