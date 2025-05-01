from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from keyboards.bread_keyboard import bread_keyboard
from keyboards.quantity_keyboard import quantity_keyboard
from bread_data import BREADS

# Состояния
CHOOSING_BREAD = 1
CHOOSING_QUANTITY = 2
ORDER_CONFIRMATION = 3

# Функция для начала заказа
async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выберите хлеб:", reply_markup=bread_keyboard)
    return CHOOSING_BREAD

# Обработчик для выбора хлеба
async def choose_bread(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    selected_bread = query.data.split('_')[1]
    context.user_data['bread'] = selected_bread  # Сохраняем выбор пользователя

    # Отправляем кнопки для выбора количества
    await query.edit_message_text(f"Вы выбрали {selected_bread}. Сколько буханок хотите?")
    await query.message.reply_text("Выберите количество:", reply_markup=quantity_keyboard)
    return CHOOSING_QUANTITY

# Обработчик для выбора количества
async def choose_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    quantity = int(query.data)  # Получаем количество

    bread = context.user_data['bread']  # Получаем выбранный хлеб
    context.user_data['quantity'] = quantity  # Сохраняем количество

    # Отправляем кнопку для подтверждения заказа
    total_price = BREADS[bread] * quantity
    await query.edit_message_text(f"Вы выбрали {quantity} буханок {bread}. Общая сумма: {total_price}€. Подтвердите заказ.")
    await query.message.reply_text("Оформить заказ?", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Оформить заказ", callback_data="confirm_order")]
    ]))
    return ORDER_CONFIRMATION

# Подтверждение заказа
async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    bread = context.user_data['bread']
    quantity = context.user_data['quantity']
    price = BREADS[bread] * quantity

    # Подтверждаем заказ
    await query.edit_message_text(f"Ваш заказ: {quantity} буханок {bread}. Общая сумма: {price}€. Заказ оформлен!")

    # Завершаем заказ
    # Здесь можно добавить отправку сообщения владельцу или сохранить заказ в базе данных
    return ConversationHandler.END
