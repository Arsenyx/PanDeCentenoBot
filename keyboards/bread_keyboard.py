# bread_keyboard.py
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from bread_data import BREADS

# Генерация кнопок для выбора хлеба
bread_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(name.capitalize(), callback_data=f"bread_{name}")] for name in BREADS
])