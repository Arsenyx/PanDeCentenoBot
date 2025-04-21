from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler
)
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
import locale

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
OWNER_CHAT_ID = int(os.getenv("OWNER_CHAT_ID"))

# Состояния
(
    MAIN_MENU,
    SELECT_BREAD,
    SELECT_QUANTITY,
    CONFIRM_ORDER,
    GET_ADDRESS,
    GET_PHONE,
    PAYMENT_METHOD
) = range(7)

# Данные о хлебе
BREADS = {
    "бородинский": 6,
    "украинский": 4,
    "дарницкий": 5
}

# Основная клавиатура
main_keyboard = ReplyKeyboardMarkup([
    ["Сделать заказ 🥯", "Меню 📋", "Помощь ❓"]
], resize_keyboard=True)

# Клавиатура выбора количества
quantity_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 4)]
])

def validate_address(address: str) -> bool:
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "addressdetails": 1, "limit": 1}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if not data:
            return False
        city = data[0].get("address", {}).get("city", "").lower()
        return city in ["valencia", "valència"]
    except Exception as e:
        print(f"Error validating address: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать в хлебную лавку! 🥯", reply_markup=main_keyboard)
    return MAIN_MENU

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_text = "Меню:\n" + "\n".join([f"· {name.capitalize()}: {price}€ (750гр)" for name, price in BREADS.items()])
    await update.message.reply_text(menu_text, reply_markup=main_keyboard)
    return MAIN_MENU

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Как заказать:\n1. Нажмите 'Сделать заказ'\n2. Выберите хлеб и количество\n3. Подтвердите заказ\n4. Укажите контакты\nМинимум 3 батона для доставки",
        reply_markup=main_keyboard
    )
    return MAIN_MENU

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

    if query.data == "add_more":
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(name.capitalize(), callback_data=name)] for name in BREADS])
        await query.edit_message_text("Выберите хлеб:", reply_markup=keyboard)
        return SELECT_BREAD

    total = sum(context.user_data['cart'].values())
    context.user_data['total'] = total

    if total >= 3:
        keyboard = ReplyKeyboardMarkup([
            ["Отправить геопозицию 📍"],
            ["Ввести адрес текстом"]
        ], resize_keyboard=True, one_time_keyboard=True)
        await query.edit_message_text("Выберите способ указания адреса:", reply_markup=keyboard)
        return GET_ADDRESS
    else:
        await query.edit_message_text("Введите контактный телефон:")
        return GET_PHONE

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address = update.message.text.strip()
    if not validate_address(address):
        await update.message.reply_text("❌ Адрес должен быть в пределах города Валенсия.")
        return GET_ADDRESS
    context.user_data['address'] = address
    await update.message.reply_text("Введите контактный телефон:")
    return GET_PHONE

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"lat": location.latitude, "lon": location.longitude, "format": "json", "addressdetails": 1}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        city = data.get("address", {}).get("city", "").lower()
        if city in ["valencia", "valència"]:
            context.user_data['address'] = data.get("display_name")
            await update.message.reply_text(f"✅ Адрес подтвержден: {data['display_name']}\nВведите контактный телефон:")
            return GET_PHONE
        else:
            await update.message.reply_text("❌ Ваша геопозиция не в Валенсии. Введите адрес вручную.")
            return GET_ADDRESS
    except Exception as e:
        print(f"Error handling location: {e}")
        await update.message.reply_text("Ошибка при проверке геопозиции. Введите адрес вручную.")
        return GET_ADDRESS

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    keyboard = ReplyKeyboardMarkup([
        ["Наличные", "Карта"]
    ], resize_keyboard=True)
    await update.message.reply_text("Выберите способ оплаты:", reply_markup=keyboard)
    return PAYMENT_METHOD

async def payment_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['payment'] = update.message.text
    cart = context.user_data['cart']
    total = sum(BREADS[bread] * qty for bread, qty in cart.items())

    try:
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'Russian_Russia')
        except:
            locale.setlocale(locale.LC_TIME, '')

    prep_time = 36 if 'бородинский' in cart else 24
    ready_time = datetime.now() + timedelta(hours=prep_time)

    def round_to_delivery_window(dt):
        start_hour, end_hour = 11, 20
        delivery_start = dt.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        delivery_end = dt.replace(hour=end_hour, minute=0, second=0, microsecond=0)
        if dt < delivery_start:
            return delivery_start
        elif dt > delivery_end:
            return (dt + timedelta(days=1)).replace(hour=start_hour)
        return dt

    pickup_time = round_to_delivery_window(ready_time)
    pickup_text = pickup_time.strftime("к %H:%M %A, %d %B %Y года").capitalize()

    await update.message.reply_text(
        f"✅ Заказ принят!\nСумма: {total}€\nГотовность: {pickup_text}\nДетали отправлены Пекарю",
        reply_markup=main_keyboard
    )

    admin_message = (
        f"🔥 НОВЫЙ ЗАКАЗ 🔥\n"
        f"Пользователь: @{update.effective_user.username}\n"
        f"------------------------------\n" +
        "\n".join([f"{name.capitalize()}: {qty} шт." for name, qty in cart.items()]) +
        f"\nСумма: {total}€\n"
        f"------------------------------\n"
        f"Оплата: {context.user_data['payment']}\n"
        f"Адрес: {context.user_data.get('address', 'Valencia 46019 Carrer de Domènec Gómez 9')}\n"
        f"Телефон: {context.user_data['phone']}\n"
        f"Готовность: {pickup_text}"
    )
    await context.bot.send_message(OWNER_CHAT_ID, admin_message)
    return MAIN_MENU

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Заказ отменен", reply_markup=main_keyboard)
    return MAIN_MENU

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                MessageHandler(filters.Regex("^Сделать заказ"), start_order),
                MessageHandler(filters.Regex("^Меню"), show_menu),
                MessageHandler(filters.Regex("^Помощь"), help_command)
            ],
            SELECT_BREAD: [CallbackQueryHandler(select_bread)],
            SELECT_QUANTITY: [CallbackQueryHandler(select_quantity)],
            CONFIRM_ORDER: [CallbackQueryHandler(confirm_order)],
            GET_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_address),
                MessageHandler(filters.LOCATION, handle_location)
            ],
            GET_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            PAYMENT_METHOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, payment_method)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )

    app.add_handler(conv_handler)
    app.run_polling()
