from telegram import ReplyKeyboardMarkup
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update, context):
    logging.info("/start command called")

    # Создаем клавиатуру с кнопками
    keyboard = [["Сделать заказ", "Меню", "Помощь"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Отправляем приветственное сообщение
    await update.message.reply_text(
        "Добро пожаловать! Выберите действие:",
        reply_markup=reply_markup
    )