from telegram import InlineKeyboardMarkup, InlineKeyboardButton  # Добавляем импорт
from telegram.ext import CallbackQueryHandler
from utils.localization import get_translation
from keyboards.main_keyboard import get_main_keyboard  # Импортируем функцию для основной клавиатуры

# Функция для смены языка
def change_language(update, context):
    query = update.callback_query
    query.answer()  # Уведомляем Telegram о том, что запрос обработан

    # Получаем текущий язык пользователя, если он есть
    user_language = context.user_data.get('language', 'ru')  # по умолчанию 'ru'

    # Кнопки для выбора языка
    language_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(get_translation('ru', 'order'), callback_data="set_language_ru")],
        [InlineKeyboardButton(get_translation('es', 'order'), callback_data="set_language_es")],
        [InlineKeyboardButton(get_translation('en', 'order'), callback_data="set_language_en")],
        [InlineKeyboardButton(get_translation('de', 'order'), callback_data="set_language_de")]
    ])
    
    # Отправляем сообщение с выбором языка
    query.edit_message_text(
        text=get_translation(user_language, 'change_language'),
        reply_markup=language_keyboard
    )

# Функция для установки языка
def set_language(update, context):
    query = update.callback_query
    language_code = query.data.split("_")[2]  # Получаем код языка из callback_data
    query.answer()

    # Сохраняем выбранный язык
    context.user_data['language'] = language_code  # Сохраняем язык для пользователя

    # Обновляем клавиатуру в зависимости от выбранного языка
    updated_main_keyboard = get_main_keyboard(language_code)  # Используем нашу функцию для обновленной клавиатуры

    # Отправляем сообщение с новым языком и обновленной клавиатурой
    query.edit_message_text(text=get_translation(language_code, 'change_language'))
    query.edit_message_reply_markup(reply_markup=updated_main_keyboard)  # Обновляем клавиатуру

# Функция возвращает обработчики
def language_handlers():
    return [
        CallbackQueryHandler(change_language, pattern='^change_language$'),
        CallbackQueryHandler(set_language, pattern='^set_language_.*$')
    ]
