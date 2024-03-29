import datetime

class Booking:
    time_format_string = "%-I:%M %p"
    date_format_string = "%a, %-d %b"
    open_time = datetime.time(8, 0)
    close_time = datetime.time(0, 0)
    
    @staticmethod
    def is_valid_start_time(hour):
        time = datetime.time(hour, 0)
        if Booking.open_time <= time:
            return True
        return False
    
    @staticmethod
    def is_more_than_24h(date, hour, min):
        if datetime.datetime.combine(date, datetime.time(hour, min)) >= datetime.datetime.now() + datetime.timedelta(days=1):
            return True
        return False
    
    @staticmethod
    def is_valid_end_time(time):
        if Booking.open_time < time or time <= Booking.close_time:
            return True
        return False

    @staticmethod
    def calculate_end_time(start_time, duration):
        return (datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(hours=duration)).time()
        
    def __init__(self, telegram_handle, date, start_time, duration, approved):
        self.telegram_handle = telegram_handle
        self.date = date
        self.start_time = start_time
        self.duration = duration
        self.approved = approved
        self.end_time = Booking.calculate_end_time(start_time, duration) if start_time and duration else None

    def __str__(self):
        date_str = self.date.strftime(Booking.date_format_string) if self.date else "NO DATE"
        start_time_str = self.start_time.strftime(Booking.time_format_string) if self.start_time else "time not set"
        end_time_str = (" to " + self.end_time.strftime(Booking.time_format_string)) if self.end_time else ""

        return date_str + ": " + start_time_str + end_time_str
    
    def __eq__(self, other):
        if isinstance(other, Booking):
            return self.telegram_handle == other.telegram_handle and self.date == other.date and self.start_time == other.start_time and self.duration == other.duration and self.approved == other.approved
        return False
    
    def get_status(self):
        if self.approved:
            return "approved"
        if self.duration is not None:
            return "unapproved"
        if self.start_time is None:
            return "setting time"
        if self.duration is None:
            return "setting duration"