from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.localization import get_translation  # Импортируем функцию для локализации

def get_main_keyboard(language_code='ru'):
    """Функция для создания клавиатуры с учётом выбранного языка"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_translation(language_code, 'order'), callback_data="order"),
         InlineKeyboardButton(get_translation(language_code, 'menu'), callback_data="menu"),
         InlineKeyboardButton(get_translation(language_code, 'help'), callback_data="help"),
         InlineKeyboardButton(get_translation(language_code, 'change_language'), callback_data="change_language")]  # Кнопка для смены языка
    ])
