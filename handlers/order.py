# handlers/order.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from bread_data import BREADS
from keyboards.quantity_keyboard import quantity_keyboard
from keyboards.bread_keyboard import bread_keyboard

# Импортируем состояния из main.py
from main import MAIN_MENU, SELECT_BREAD, SELECT_QUANTITY, CONFIRM_ORDER, GET_PHONE

async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['cart'] = {}
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(name.capitalize(), callback_data=name)] for name in BREADS])
    await update.message.reply_text("Выберите хлеб:", reply_markup=keyboard)
    return SELECT_BREAD

async def select_bread(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['current_bread'] = query.data
    await query.edit_message_text(f"Выберите количество для {query.data.capitalize()} (max 3):", reply_markup=quantity_keyboard)
    return SELECT_QUANTITY

async def select_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    quantity = int(query.data)
    bread = context.user_data['current_bread']
    cart = context.user_data['cart']
    cart[bread] = cart.get(bread, 0) + quantity
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Добавить еще", callback_data="add_more"),
         InlineKeyboardButton("Подтвердить", callback_data="confirm")]
    ])
    await query.edit_message_text(
        f"Добавлено: {bread.capitalize()} × {quantity}\nЧто дальше?",
        reply_markup=keyboard
    )
    return CONFIRM_ORDER

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cart = context.user_data['cart']
    total = sum(BREADS[bread] * qty for bread, qty in cart.items())

    # Handle confirmation, ask for address or phone
    await query.edit_message_text(f"Сумма: {total}€\nПодтвердите заказ!")

    # Запрашиваем номер телефона у пользователя
    return GET_PHONE
