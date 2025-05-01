from telegram import InlineKeyboardMarkup, InlineKeyboardButton

quantity_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 4)]
])