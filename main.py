# Conversation states
# MAIN_MENU, SELECT_BREAD, SELECT_QUANTITY, CONFIRM_ORDER = range(4)

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
# from config import TOKEN, MAIN_MENU, SELECT_BREAD, SELECT_QUANTITY, CONFIRM_ORDER

from handlers.start import start
from handlers.menu import show_menu
from handlers.help import help_command
from handlers.cancel import cancel

from handlers.order import (
    start_order,
    select_bread,
    select_quantity,
    confirm_order
)

from utils.address_validation import validate_location
from utils.localy_setup import set_language
from utils.delivery_time import get_delivery_time
from utils.address_validation import get_phone, payment_method
from config import TOKEN
from states import (
    MAIN_MENU,
    SELECT_BREAD,
    SELECT_QUANTITY,
    CONFIRM_ORDER
)
from keyboards.bread_keyboard import bread_keyboard
from keyboards.quantity_keyboard import quantity_keyboard
from keyboards.main_keyboard import main_keyboard
from keyboards.main_keyboard import main_keyboard   

async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, выберите опцию из меню.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Сделать заказ"), start_order)],
        states={
            SELECT_BREAD: [CallbackQueryHandler(select_bread)],
            SELECT_QUANTITY: [CallbackQueryHandler(select_quantity)],
            CONFIRM_ORDER: [CallbackQueryHandler(confirm_order)],
            MAIN_MENU: [
                MessageHandler(filters.LOCATION, validate_location),
                MessageHandler(filters.CONTACT, get_phone),
                MessageHandler(filters.TEXT & ~filters.COMMAND, payment_method)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            MessageHandler(filters.TEXT, fallback)
        ]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", show_menu))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(conv_handler)

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
