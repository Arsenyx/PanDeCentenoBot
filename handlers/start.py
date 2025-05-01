from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

# from config import MAIN_MENU  # Состояние лучше хранить в config.py
from states import MAIN_MENU


main_keyboard = ReplyKeyboardMarkup([
    ["Сделать заказ 🥯", "Меню 📋", "Помощь ❓"]
], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в хлебную лавку! 🥯\nВыберите действие:",
        reply_markup=main_keyboard
    )
    return MAIN_MENU
