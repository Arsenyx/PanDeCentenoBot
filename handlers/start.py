from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update, context):
    logging.info("/start command called")

    # Создаем inline-кнопку для начала заказа
    keyboard = [
        [InlineKeyboardButton("Сделать заказ", callback_data="make_order")],  # Inline-кнопка с callback_data
        [InlineKeyboardButton("Меню", callback_data="menu")],
        [InlineKeyboardButton("Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем приветственное сообщение с inline-кнопками
    await update.message.reply_text(
        "Добро пожаловать! Выберите действие:",
        reply_markup=reply_markup
    )
