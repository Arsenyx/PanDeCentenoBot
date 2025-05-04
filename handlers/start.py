from telegram import Update
from telegram.ext import ContextTypes
from keyboards.main_keyboard import get_main_keyboard
from utils.localization import detect_language_code  # если есть

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language_code = detect_language_code(update) if callable(detect_language_code) else 'ru'
    await update.message.reply_text(
        "Добро пожаловать! Выберите действие:",
        reply_markup=get_main_keyboard(language_code)
    )

