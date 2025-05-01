from telegram import Update
from telegram.ext import ContextTypes
from keyboards.main_keyboard import main_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡ 🍞 Добро пожаловать в хлебную лавку 🍞! ", reply_markup=main_keyboard)
    return 1  # MAIN_MENU