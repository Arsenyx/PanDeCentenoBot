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

# Функция проверки адреса через OpenStreetMap Nominatim
def validate_address(address: str) -> bool:
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "addressdetails": 1,
        "limit": 1
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if not data:
            return False
        
        # Извлекаем информацию о городе
        city = data[0].get("address", {}).get("city", "").lower()
        return city == "valencia" or city == "valència"  # Учитываем оба варианта написания
    
    except Exception as e:
        print(f"Error validating address: {e}")
        return False

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в хлебную лавку! 🥯",
        reply_markup=main_keyboard
    )
    return MAIN_MENU

# Показ меню
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_text = "Меню:\n" + "\n".join([
        f"· {name.capitalize()}: {price}€ 750гр)" 
        for name, price in BREADS.items()
    ])
    await update.message.reply_text(menu_text, reply_markup=main_keyboard)
    return MAIN_MENU

# Помощь
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Как заказать:\n"
        "1. Нажмите 'Сделать заказ'\n"
        "2. Выберите хлеб и количество\n"
        "3. Подтвердите заказ\n"
        "4. Укажите контакты\n"
        "Минимум 3 батона для доставки"
    )
    await update.message.reply_text(help_text, reply_markup=main_keyboard)
    return MAIN_MENU

# Начало заказа
async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['cart'] = {}
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(name.capitalize(), callback_data=name)] 
        for name in BREADS.keys()
    ])
    await update.message.reply_text(
        "Выберите хлеб:",
        reply_markup=keyboard
    )
    return SELECT_BREAD

# Выбор хлеба
async def select_bread(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    bread = query.data
    context.user_data['current_bread'] = bread
    await query.edit_message_text(
        f"Выберите количество для {bread.capitalize()} (max 3):",
        reply_markup=quantity_keyboard
    )
    return SELECT_QUANTITY

# Выбор количества
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
        f"Добавлено: {bread.capitalize()} × {quantity}\n"
        "Что дальше?",
        reply_markup=keyboard
    )
    return CONFIRM_ORDER

# Подтверждение заказа
async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "add_more":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(name.capitalize(), callback_data=name)] 
            for name in BREADS.keys()
        ])
        await query.edit_message_text(
            "Выберите хлеб:",
            reply_markup=keyboard
        )
        return SELECT_BREAD
    
    total = sum(context.user_data['cart'].values())
    context.user_data['total'] = total
    
    if total >= 3:
        keyboard = ReplyKeyboardMarkup([
            ["Отправить геопозицию 📍"],
            ["Ввести адрес текстом"]
        ], resize_keyboard=True, one_time_keyboard=True)
        await query.edit_message_text(
            "Выберите способ указания адреса:",
            reply_markup=keyboard
        )
        return GET_ADDRESS
    else:
        await query.edit_message_text("Введите контактный телефон:")
        return GET_PHONE

# Получение адреса текстом
async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address = update.message.text.strip()
    
    # Проверяем, принадлежит ли адрес Валенсии
    if not validate_address(address):
        await update.message.reply_text(
            "❌ Адрес должен быть в пределах города Валенсия. Пожалуйста, укажите корректный адрес."
        )
        return GET_ADDRESS
    
    context.user_data['address'] = address
    await update.message.reply_text("Введите контактный телефон:")
    return GET_PHONE

# Обработка геолокации
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    latitude = location.latitude
    longitude = location.longitude
    
    # Проверяем город через геокодинг
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": latitude,
        "lon": longitude,
        "format": "json",
        "addressdetails": 1
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        city = data.get("address", {}).get("city", "").lower()
        
        if city == "valencia" or city == "valència":
            context.user_data['address'] = data.get("display_name")
            await update.message.reply_text(
                f"✅ Адрес подтвержден: {data['display_name']}\nВведите контактный телефон:"
            )
            return GET_PHONE
        else:
            await update.message.reply_text(
                "❌ Ваша геопозиция не находится в Валенсии. Пожалуйста, укажите другой адрес."
            )
            return GET_ADDRESS
    
    except Exception as e:
        print(f"Error handling location: {e}")
        await update.message.reply_text("Ошибка при проверке геопозиции. Пожалуйста, введите адрес текстом.")
        return GET_ADDRESS

# Получение телефона
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    keyboard = ReplyKeyboardMarkup([
        ["Наличные", "Карта"]
    ], resize_keyboard=True)
    await update.message.reply_text(
        "Выберите способ оплаты:",
        reply_markup=keyboard
    )
    return PAYMENT_METHOD

# Способ оплаты
async def payment_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['payment'] = update.message.text
    cart = context.user_data['cart']
    total = sum(BREADS[bread] * qty for bread, qty in cart.items())
    prep_time = 36 if 'бородинский' in cart else 24
    
    # Сообщение пользователю
    user_message = (
        f"✅ Заказ принят!\n"
        f"Сумма: {total}€\n"
        f"Готовность через: {prep_time} часов\n"
        f"Детали отправлены администратору"
    )
    await update.message.reply_text(user_message, reply_markup=main_keyboard)
    
    # Сообщение админу
    admin_message = (
        f"🔥 НОВЫЙ ЗАКАЗ 🔥\n"
        f"Пользователь: @{update.effective_user.username}\n"
        f"------------------------------\n"
        + "\n".join([
            f"{name.capitalize()}: {qty} шт." 
            for name, qty in cart.items()
        ]) +
        f"\nСумма: {total}€\n"
        f"------------------------------\n"
        f"Оплата: {context.user_data['payment']}\n"
        f"Адрес: {context.user_data.get('address', 'Самовывоз')}\n"
        f"Телефон: {context.user_data['phone']}\n"
        f"Готовность: {prep_time} часов"
    )
    await context.bot.send_message(OWNER_CHAT_ID, admin_message)
    
    return MAIN_MENU

# Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Заказ отменен",
        reply_markup=main_keyboard
    )
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
        SELECT_BREAD: [CallbackQueryHandler(select_bread)],  # Убран параметр per_message
#       SELECT_BREAD: [CallbackQueryHandler(select_bread, per_message=True)],
        SELECT_QUANTITY: [CallbackQueryHandler(select_quantity)],  # Убран параметр per_message
#       SELECT_QUANTITY: [CallbackQueryHandler(select_quantity, per_message=True)],
        CONFIRM_ORDER: [CallbackQueryHandler(confirm_order)],  # Убран параметр per_message
#       CONFIRM_ORDER: [CallbackQueryHandler(confirm_order, per_message=True)],
        GET_ADDRESS: [
            MessageHandler(filters.TEXT, get_address),
            MessageHandler(filters.LOCATION, handle_location)
        ],
        GET_PHONE: [MessageHandler(filters.TEXT, get_phone)],
        PAYMENT_METHOD: [MessageHandler(filters.TEXT, payment_method)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    allow_reentry=True
)

    app.add_handler(conv_handler)
    app.run_polling()
