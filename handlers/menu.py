from telegram import Update
from telegram.ext import ContextTypes
from bread_data import BREADS
from keyboards.main_keyboard import main_keyboard

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_text = "Меню:\n" + "\n".join([f"· {name.capitalize()}: {price}€ (750гр)" for name, price in BREADS.items()])
    await update.message.reply_text(menu_text, reply_markup=main_keyboard)
    return 0  # MAIN_MENU