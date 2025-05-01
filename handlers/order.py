from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from keyboards.bread_keyboard import bread_keyboard
from keyboards.quantity_keyboard import quantity_keyboard
from bread_data import BREADS
import logging

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Состояния
CHOOSING_BREAD = 1
CHOOSING_QUANTITY = 2
ORDER_CONFIRMATION = 3

# Функция для начала заказа
async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Ответить на callback-запрос

    logging.info("start_order called")

    # Отправляем сообщение с клавиатурой для выбора хлеба
    await query.message.reply_text("Выберите хлеб:", reply_markup=bread_keyboard)
    return CHOOSING_BREAD  # Переход к следующему состоянию