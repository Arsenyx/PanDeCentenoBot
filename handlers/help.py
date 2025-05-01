from telegram import Update
from telegram.ext import ContextTypes
from keyboards.main_keyboard import main_keyboard

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Как заказать:\n1. Нажмите 'Сделать заказ'\n2. Выберите хлеб и количество\n3. Подтвердите заказ\n4. Укажите контакты\nМинимум 3 батона для доставки",
        reply_markup=main_keyboard
    )
    return 0  # MAIN_MENU