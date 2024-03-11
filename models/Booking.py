from datetime import date, datetime, timedelta

class Booking:
    time_format_string = "%-I:%M %p"
    date_format_string = "%a, %-d %b"
    
    @staticmethod
    def is_valid_start_time(hour):
        if hour > 7 and hour < 24:
            return True
        return False
    
    @staticmethod
    def is_valid_end_time(hour, min):
        if Booking.is_valid_start_time(hour) or (hour == 0 and min == 0):
            return True
        return False

    def calculate_end_time(self, start_time, duration):
        return (datetime.combine(date.today(), start_time) + timedelta(hours=duration)).time()
        
    def __init__(self, telegram_handle, date, start_time, duration, approved):
        self.telegram_handle = telegram_handle
        self.date = date
        self.start_time = start_time
        self.duration = duration
        self.approved = approved
        self.end_time = self.calculate_end_time(start_time, duration) if start_time and duration else None

    def __str__(self):
        date_str = self.date.strftime(Booking.date_format_string) if self.date else "NO DATE"
        start_time_str = self.start_time.strftime(Booking.time_format_string) if self.start_time else "NO START TIME"
        end_time_str = self.end_time.strftime(Booking.time_format_string) if self.end_time else "NO DURATION/END TIME"

        return date_str + ": " + start_time_str + " to " + end_time_str