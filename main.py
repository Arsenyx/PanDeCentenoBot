from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ConversationHandler, ContextTypes, filters
)
from telegram import Update
from config import TOKEN
from handlers.start import start
from handlers.menu import show_menu
from handlers.help import help_command
from handlers.language import language_handlers
from handlers.cancel import cancel
from handlers.order import start_order, select_bread, select_quantity, confirm_order
from utils.address_validation import validate_address, get_phone, payment_method
from states import MAIN_MENU, SELECT_BREAD, SELECT_QUANTITY, CONFIRM_ORDER

# Функция для fallback
async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, выберите опцию из меню.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Обработчики языков (inline)
    for handler in language_handlers():
        app.add_handler(handler)

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", show_menu))
    app.add_handler(CommandHandler("help", help_command))

    # Обработка ReplyKeyboard текста (главное меню)
    app.add_handler(MessageHandler(filters.Regex("^📋 Меню$"), show_menu))
    app.add_handler(MessageHandler(filters.Regex("^ℹ️ Помощь$"), help_command))
    app.add_handler(MessageHandler(filters.Regex("^🛒 Сделать заказ$"), start_order))

    # Заказ (через ConversationHandler)
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^🛒 Сделать заказ$"), start_order)],
        states={
            SELECT_BREAD: [CallbackQueryHandler(select_bread)],
            SELECT_QUANTITY: [CallbackQueryHandler(select_quantity)],
            CONFIRM_ORDER: [CallbackQueryHandler(confirm_order)],
            MAIN_MENU: [
                MessageHandler(filters.LOCATION, validate_address),
                MessageHandler(filters.CONTACT, get_phone),
                MessageHandler(filters.TEXT & ~filters.COMMAND, payment_method),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            MessageHandler(filters.TEXT, fallback)
        ]
    )
    app.add_handler(conv_handler)

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
