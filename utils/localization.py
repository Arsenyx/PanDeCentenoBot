# Словарь для локализации
LANGUAGES = {
    'ru': {
        'order': 'Сделать заказ 🍞',
        'menu': 'Меню 📋',
        'help': 'Помощь ❓',
        'change_language': 'Сменить язык 🌐',
    },
    'es': {
        'order': 'Hacer pedido 🍞',
        'menu': 'Menú 📋',
        'help': 'Ayuda ❓',
        'change_language': 'Cambiar idioma 🌐',
    },
    'en': {
        'order': 'Place order 🍞',
        'menu': 'Menu 📋',
        'help': 'Help ❓',
        'change_language': 'Change language 🌐',
    },
    'de': {
        'order': 'Bestellung aufgeben 🍞',
        'menu': 'Menü 📋',
        'help': 'Hilfe ❓',
        'change_language': 'Sprache ändern 🌐',
    }
}

# Функция для получения перевода на основе языка
def get_translation(language_code, key):
    # Если для указанного языка есть перевод, возвращаем его, иначе перевод на русский (по умолчанию)
    return LANGUAGES.get(language_code, LANGUAGES['ru']).get(key, key)
