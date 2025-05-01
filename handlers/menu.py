from telegram import Update
from telegram.ext import ContextTypes
from bread_data import BREADS
from keyboards.main_keyboard import get_main_keyboard
from utils.localization import detect_language_code  # если у тебя есть такая функция

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language_code = detect_language_code(update) if callable(detect_language_code) else 'ru'
    menu_text = "Меню:\n" + "\n".join([f"· {name.capitalize()}: {price}€ (750гр)" for name, price in BREADS.items()])
    await update.message.reply_text(menu_text, reply_markup=get_main_keyboard(language_code))
    return 0  # MAIN_MENU
