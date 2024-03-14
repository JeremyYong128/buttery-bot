import datetime
import json
import re

def generate_dates_keyboard_markup():
    keyboard = [[ generate_keyboard_date_button(i, j) for j in range(2)] for i in range(4)]
    return json.dumps({
        "inline_keyboard": keyboard
    })

def generate_keyboard_date_button(row, col):
    value = 2 * row + col
    date = datetime.date.today() + datetime.timedelta(days=value)
    day = str(date.day)
    month = str(date.month)
    year = str(date.year)
    date_string = format_booking_date(date)
    
    return {
        "text": date_string,
        "callback_data": " ".join((day, month, year))
    }

def yes_no_keyboard_markup():
    return json.dumps({
        "inline_keyboard": [[{
            "text": "Confirm",
            "callback_data": "Confirm"
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