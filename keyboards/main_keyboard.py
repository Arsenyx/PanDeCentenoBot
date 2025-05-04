from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard(language_code="ru"):
    if language_code == "es":
        buttons = [["📋 Menú", "ℹ️ Ayuda"], ["🛒 Hacer pedido", "🌐 Idioma"]]
    elif language_code == "de":
        buttons = [["📋 Menü", "ℹ️ Hilfe"], ["🛒 Bestellung", "🌐 Sprache"]]
    elif language_code == "en":
        buttons = [["📋 Menu", "ℹ️ Help"], ["🛒 Order", "🌐 Language"]]
    else:  # ru
        buttons = [["📋 Меню", "ℹ️ Помощь"], ["🛒 Сделать заказ", "🌐 Язык"]]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
