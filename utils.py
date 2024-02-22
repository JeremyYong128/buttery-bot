from datetime import date, timedelta
import json

def generate_dates_keyboard_markup():
    keyboard = [[ generate_keyboard_date_button(i, j) for j in range(2)] for i in range(4)]
    return json.dumps({
        "inline_keyboard": keyboard
    })

def generate_keyboard_date_button(row, col):
    value = 2 * row + col
    date_string = format_booking_date(date.today() + timedelta(days=value))
    
    return {
        "text": date_string,
        "callback_data": value
    }

def format_booking_date(date):
    return date.strftime("%-d %b")