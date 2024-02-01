from datetime import timedelta
from datetime import datetime
from datetime import date

class Booking:
    time_format_string = "%-I:%M %p"
    date_format_string = "%a, %-d %b"
        
    def __init__(self, telegram_handle, date, start_time, duration):
        self.telegram_handle = telegram_handle
        self.date = date
        self.start_time = start_time
        self.duration = duration
        self.end_time = calculate_end_time(start_time, duration)

    def __str__(self):
        date_str = self.date.strftime(Booking.date_format_string)
        start_time_str = self.strftime(Booking.time_format_string)
        end_time_str = self.strftime(Booking.time_format_string)

        return date_str + ": " + start_time_str + " to " + end_time_str

    def calculate_end_time(start_time, duration):
        return datetime.combine(date.today(), start_time) + timedelta(duration).time()