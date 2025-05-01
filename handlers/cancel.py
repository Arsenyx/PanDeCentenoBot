from telegram import Update
from telegram.ext import ContextTypes
from keyboards.main_keyboard import main_keyboard

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Заказ отменен", reply_markup=main_keyboard)
    return 0  # MAIN_MENU
