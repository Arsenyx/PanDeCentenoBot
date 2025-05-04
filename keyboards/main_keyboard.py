from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard(language_code="ru"):
    if language_code == "es":
        buttons = [["📋 Menú", "ℹ️ Ayuda"], ["🛒 Hacer pedido", "🌐 Idioma"]]
    else:
        buttons = [["📋 Меню", "ℹ️ Помощь"], ["🛒 Сделать заказ", "🌐 Язык"]]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

