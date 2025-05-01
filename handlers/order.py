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

# Обработчик для выбора хлеба
async def choose_bread(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Ответить на callback-запрос

    selected_bread = query.data.split('_')[1]  # Извлекаем выбор хлеба
    context.user_data['bread'] = selected_bread  # Сохраняем выбор

    logging.info(f"User selected bread: {selected_bread}")

    # Отправляем сообщение с предложением выбрать количество
    await query.edit_message_text(f"Вы выбрали {selected_bread}. Сколько буханок хотите?")
    await query.message.reply_text("Выберите количество:", reply_markup=quantity_keyboard)
    return CHOOSING_QUANTITY  # Переход к следующему состоянию

# Обработчик для выбора количества
async def choose_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Ответить на callback-запрос

    quantity = int(query.data)  # Получаем выбранное количество
    bread = context.user_data['bread']  # Получаем выбранный хлеб
    context.user_data['quantity'] = quantity  # Сохраняем количество

    logging.info(f"User selected quantity: {quantity}")

    # Вычисляем общую сумму
    total_price = BREADS[bread] * quantity
    await query.edit_message_text(f"Вы выбрали {quantity} буханок {bread}. Общая сумма: {total_price}€. Подтвердите заказ.")
    await query.message.reply_text("Оформить заказ?", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Оформить заказ", callback_data="confirm_order")]
    ]))
    return ORDER_CONFIRMATION  # Переход к следующему состоянию

# Подтверждение заказа
async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Ответить на callback-запрос

    bread = context.user_data['bread']
    quantity = context.user_data['quantity']
    price = BREADS[bread] * quantity

    logging.info(f"Order confirmed: {quantity} x {bread}")

    # Подтверждаем заказ
    await query.edit_message_text(f"Ваш заказ: {quantity} буханок {bread}. Общая сумма: {price}€. Заказ оформлен!")

    # Завершаем заказ
    # Здесь можно добавить отправку сообщения владельцу или сохранить заказ в базе данных

    return ConversationHandler.END  # Завершаем разговор