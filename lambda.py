import json
import message
import database
import utils
import datetime
from functools import reduce
from models.Booking import Booking

def handler(event, context):
    update = json.loads(event['body'])
    print(update)
    database.update()

    if 'message' in update:
        if update['message']['chat']['type'] == 'private':
            handle_private_message(update)

        if update['message']['chat']['type'] == 'group':
            handle_group_message(update)

    if 'callback_query' in update:
        handle_callback(update)
    
    return {
        'statusCode': 200
    }

def handle_private_message(update):
    chat_id = str(update['message']['chat']['id'])
    command = update['message']['text'] if 'text' in update['message'] else None
    handle = update['message']['from']['username']
    user_status = database.get_user_status(handle)
  
    if command == '/start':
        message.send(chat_id, "Welcome to Saga Buttery Bot!\n\n" + message.COMMAND_LIST)
        return
        
    if command == '/help':
        message.send(chat_id, message.COMMAND_LIST + "\n\n" + message.GUIDELINES + "\n\nFor more assistance, contact @carinateh, @jemmacheah, @jeremyyong128, @owenyeoo, or @ymirmeddeb.")
        return
    
    if command == '/bookings':
        bookings = database.get_approved_bookings()
        
        if len(bookings) == 0:
            message.send(chat_id, "There are no bookings.")
        else:
            initial_str = "Here are all the current bookings:\n\n"
            final_str = reduce(lambda acc, next: acc + "\n" + str(next), bookings, initial_str)
            message.send(chat_id, final_str)
        return
    
    if command == '/mybooking':
        booking = database.get_user_booking(handle)

        if booking is None:
            message.send(chat_id, "You have no bookings.")
        elif booking.get_status() == "approved":
            message.send(chat_id, "You have one approved booking:\n\n" + str(booking))
        elif booking.get_status() == "unapproved":
            message.send(chat_id, "You have one unapproved booking:\n\n" + str(booking))
        else:
            message.send(chat_id, "You have one booking in progress:\n\n" + str(booking))
        return

    if command == '/delete':
        booking = database.get_user_booking(handle)

        if booking is None:
            message.send(chat_id, "You have no bookings. To create a booking, use /book.")
        elif booking.get_status() == "approved":
            message.send(chat_id, "You have one approved booking:\n\n" + str(booking) + "\n\nPress confirm to delete this booking.", utils.confirm_keyboard_markup())
        elif booking.get_status() == "unapproved":
            message.send(chat_id, "You have one unapproved booking:\n\n" + str(booking) + "\n\nPress confirm to delete this booking.", utils.confirm_keyboard_markup())
        else:
            message.send(chat_id, "You have one booking in progress:\n\n" + str(booking) + "\n\nPress confirm to delete this booking.", utils.confirm_keyboard_markup())
        return

    if command == '/book':
        if user_status == "approved" or user_status == "unapproved":
            message.send(chat_id, message.PREVIOUS_BOOKING_MESSAGE)
        
        else:
            keyboard_markup = utils.generate_dates_keyboard_markup()
            message.send(chat_id, "Choose the day of your booking:", keyboard_markup)
        return

    if user_status == "setting time":
        if not utils.is_valid_time_format(command):
            message.send(chat_id, "Invalid time format. Make sure it follows the 24h format and is on the hour/half hour (e.g. 23:00, 1430).")
            return

        hour, min = utils.parse_time_string(command)

        if not Booking.is_valid_start_time(hour):
            message.send(chat_id, "Invalid time provided. The start time of bookings has to be from 8am to 11:30pm (0800 - 2330).")
            return
        
        booking_date = database.get_booking_date(handle)[0]

        if not Booking.is_more_than_24h(booking_date, hour, min):
            message.send(chat_id, "Invalid time provided. Bookings have to be made at least 24h in advance.")
            return
        
        database.update_booking_time(handle, hour, min)
        message.send(chat_id, "The time of your booking has been set to " + str(hour) + ":" + (str(min) if min else "00") + ".\n\n" +
                     "Enter the duration of your booking. Note that bookings can be a maximum of 2h long, and must be in intervals of 0.5h.")
        return

    if user_status == "setting duration":
        duration = None
    
        try:
            duration = float(command)
        except ValueError:
            message.send(chat_id, "Invalid duration format. Make sure it is a valid duration (e.g. 0.5, 1).")
            return
        
        if duration % 0.5 != 0:
            message.send(chat_id, "Invalid duration provided. Duration must be in intervals of 0.5h (i.e. values like 0.75 will not be accepted).")
            return
        
        if duration >= 24:
            message.send(chat_id, "Duration is too long.")
            return
        
        booking = database.get_user_booking(handle)
        end_time = Booking.calculate_end_time(booking.start_time, duration)

        if not Booking.is_valid_end_time(end_time):
            message.send(chat_id, "Invalid duration provided. Bookings must end by 12am.")
            return

        database.update_booking_duration(handle, duration)
        message.send(chat_id, "The duration of your booking has been set to " + (str(duration) if not duration.is_integer() else str(int(duration))) + " hours.")
        booking = database.get_user_booking(handle)
        message.send(chat_id, "Your booking has been made!\n\n" + str(booking) + "\n\nYou will get a message when your booking has been approved by one of our buttery ICs.")
        message.send_to_admin("@" + handle + " has made a booking:\n\n" + str(booking), utils.admin_confirm_keyboard_markup(chat_id, handle, booking.date, booking.start_time, booking.duration))
        return
     
    message.send(chat_id, "Unknown command. Type /help for a list of commands.")

def handle_group_message(update):
    chat_id = str(update['message']['chat']['id'])

    if chat_id != message.ADMIN_CHAT_ID:
        return
    
    command = update['message']['text'] if 'text' in update['message'] else None
    
    message.send_to_admin("Group message received")


def handle_callback(update):
    chat_id = str(update['callback_query']['message']['chat']['id'])
    handle = update['callback_query']['from']['username']
    user_status = database.get_user_status(handle)
    callback_data = update['callback_query']['data'].split(" ")
    command = callback_data[0]
    data = callback_data[1:] if len(callback_data) > 1 else None

    if command == "CONFIRM":
        database.delete_booking(handle)
        message.send(chat_id, "Your booking has been deleted.")
        return
    
    if command == "BOOK":
        if user_status == "approved" or user_status == "unapproved":
            message.send(chat_id, message.PREVIOUS_BOOKING_MESSAGE)
        else:
            day, month, year = map(int, data)
            date = datetime.date(year, month, day)
            database.update_booking_date(handle, date, user_status)
            message.send(chat_id, "The date of your booking has been set to " + utils.format_booking_date(date) + ".\n\n" +
                         "Enter the time of your booking in 24h format (HH:MM or HHMM). Note that bookings can only be made on the hour or half hour.")
        return
    
    if command == "APPROVE" or command == "REJECT":
        chat_id, handle, year, month, day, hour, minute, duration = data
        date = datetime.date(int(year), int(month), int(day))
        time = datetime.time(int(hour), int(minute))
        booking = database.get_user_booking(handle)
        
        if booking != Booking(handle, date, time, float(duration), False):
            message.send_to_admin("Booking is no longer valid.")
            return
        
        if command == "APPROVE":
            database.approve_booking(handle)
            message.send_to_admin("@" + handle + "'s booking has been approved:\n\n" + str(booking))
            message.send(chat_id, "Your booking has been approved!\n\n" + str(booking))
            return
        
        if command == "REJECT":
            database.delete_booking(handle)
            message.send_to_admin("@" + handle + "'s booking has been rejected:\n\n" + str(booking))
            message.send(chat_id, "Your booking has been rejected.\n\n" + str(booking))
            return