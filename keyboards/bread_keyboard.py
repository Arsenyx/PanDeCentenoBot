from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from bread_data import BREADS

bread_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(name.capitalize(), callback_data=name)] for name in BREADS
])