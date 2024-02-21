from datetime import date, timedelta

WELCOME_MESSAGE = "Welcome to Saga Buttery Bot!"
HELP_MESSAGE = "- Type /bookings to view all bookings for the next 7 days.\n- Type /book to get started with booking the buttery."
CONTACT_MESSAGE = "For more assistance, contact @carinateh, @jemmacheah, @jeremyyong128, @owenyeoo, or @ymirmeddeb."
UNKNOWN_COMMAND_MESSAGE = "Unknown command. Please ensure you have entered the correct command."
NO_BOOKINGS_MESSAGE = "There are no bookings."

# def generate_keyboard_markup():
#     keyboard = [[ generate_keyboard_button(i, j) for j in range(2)] for i in range(4)]
#     return InlineKeyboardMarkup(keyboard)

# def generate_keyboard_button(i, j):
#     date_string = (date.today() + timedelta(days=2 * i + j)).strftime("%-d %b")
#     return InlineKeyboardButton(date_string, callback_data=date_string)