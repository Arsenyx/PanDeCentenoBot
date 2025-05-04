from telegram import Update
from telegram.ext import ContextTypes
from bread_data import BREADS
from utils.localization import detect_language_code  # если есть

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language_code = detect_language_code(update) if callable(detect_language_code) else 'ru'
    menu_text = "Меню:\n" + "\n".join([f"· {name.capitalize()}: {price}€ (750гр)" for name, price in BREADS.items()])
    await update.message.reply_text(menu_text)  # без reply_markup

    return 0
