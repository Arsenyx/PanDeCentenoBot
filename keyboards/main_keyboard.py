from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.localization import get_translation  # Импортируем функцию для локализации

# Создаем клавиатуру с кнопками на разных языках
main_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(get_translation('ru', 'order'), callback_data="order"),
     InlineKeyboardButton(get_translation('ru', 'menu'), callback_data="menu"),
     InlineKeyboardButton(get_translation('ru', 'help'), callback_data="help"),
     InlineKeyboardButton(get_translation('ru', 'change_language'), callback_data="change_language")]
])

