from datetime import timedelta
from datetime import datetime

class Booking:
    time_format_string = "%-I:%M %p"
    date_format_string = "%a, %-d %b"
        
    def __init__(self, telegram_handle, date, start_time, duration):
        self.telegram_handle = telegram_handle
        self.date = date
        self.start_time = start_time
        self.duration = duration
        self.end_time = start_time + timedelta(hours=duration)

    def __str__(self):
        date_str = self.date.strftime(Booking.date_format_string)
        start_time_str = self.strftime(Booking.time_format_string)
        end_time_str = self.strftime(Booking.time_format_string)

        return date_str + ": " + start_time_str + " to " + end_time_str