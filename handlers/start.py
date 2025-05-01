from telegram import ReplyKeyboardMarkup

async def start(update, context):
    # Создаем клавиатуру с кнопками
    keyboard = [["Сделать заказ", "Меню", "Помощь"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Отправляем приветственное сообщение
    await update.message.reply_text(
        "Добро пожаловать! Выберите действие:",
        reply_markup=reply_markup
    )