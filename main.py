# handlers/language.py
from telegram.ext import CallbackQueryHandler
from utils.localization import get_translation
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
# from keyboards.main_keyboard import main_keyboard  # Импортируем основную клавиатуру
from keyboards.main_keyboard import get_main_keyboard


# Функция для смены языка
def change_language(update, context):
    query = update.callback_query
    query.answer()  # Уведомляем Telegram о том, что запрос обработан

    # Кнопки для выбора языка
    language_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(get_translation('ru', 'order'), callback_data="set_language_ru")],
        [InlineKeyboardButton(get_translation('es', 'order'), callback_data="set_language_es")],
        [InlineKeyboardButton(get_translation('en', 'order'), callback_data="set_language_en")],
        [InlineKeyboardButton(get_translation('de', 'order'), callback_data="set_language_de")]
    ])
    
    # Отправляем сообщение с выбором языка
    query.edit_message_text(text=get_translation('ru', 'change_language'), reply_markup=language_keyboard)

# Функция для установки языка
def set_language(update, context):
    query = update.callback_query
    language_code = query.data.split("_")[2]  # Получаем код языка из callback_data
    query.answer()

    # Сохраняем выбранный язык
    user = update.effective_user
    context.user_data['language'] = language_code  # Сохраняем язык для пользователя

    # Обновляем клавиатуру в зависимости от выбранного языка
    updated_main_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(get_translation(language_code, 'order'), callback_data="order"),
         InlineKeyboardButton(get_translation(language_code, 'menu'), callback_data="menu"),
         InlineKeyboardButton(get_translation(language_code, 'help'), callback_data="help"),
         InlineKeyboardButton(get_translation(language_code, 'change_language'), callback_data="change_language")]
    ])

    # Отправляем сообщение с новым языком и обновленной клавиатурой
    query.edit_message_text(text=get_translation(language_code, 'change_language'))
    query.edit_message_reply_markup(reply_markup=updated_main_keyboard)  # Обновляем клавиатуру

# Функция возвращает обработчики
def language_handlers():
    return [
        CallbackQueryHandler(change_language, pattern='^change_language$'),
        CallbackQueryHandler(set_language, pattern='^set_language_.*$')
    ]

# main.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, ContextTypes, filters
from handlers.start import start
from handlers.menu import show_menu
from handlers.help import help_command
from handlers.cancel import cancel
from handlers.language import language_handlers
from handlers.order import start_order, select_bread, select_quantity, confirm_order
from utils.address_validation import validate_address
from utils.localy_setup import setup_locale
from utils.delivery_time import get_delivery_time
from utils.address_validation import get_phone, payment_method
from config import TOKEN
from states import MAIN_MENU, SELECT_BREAD, SELECT_QUANTITY, CONFIRM_ORDER
from keyboards.bread_keyboard import bread_keyboard
from keyboards.quantity_keyboard import quantity_keyboard
from keyboards.main_keyboard import main_keyboard

# Функция для обработки ошибок
async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, выберите опцию из меню.")

def main():
    # Создаем приложение
    app = ApplicationBuilder().token(TOKEN).build()

    # Создаем ConversationHandler с вашими состояниями
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Сделать заказ"), start_order)],
        states={
            SELECT_BREAD: [CallbackQueryHandler(select_bread)],
            SELECT_QUANTITY: [CallbackQueryHandler(select_quantity)],
            CONFIRM_ORDER: [CallbackQueryHandler(confirm_order)],
            MAIN_MENU: [
                MessageHandler(filters.LOCATION, validate_address),
                MessageHandler(filters.CONTACT, get_phone),
                MessageHandler(filters.TEXT & ~filters.COMMAND, payment_method)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            MessageHandler(filters.TEXT, fallback)
        ]
    )

    # Регистрируем обработчики для смены языка
    for handler in language_handlers():  # Регистрируем каждый обработчик по отдельности
        app.add_handler(handler)

    # Другие обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", show_menu))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(conv_handler)

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
