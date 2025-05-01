from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, CallbackQueryHandler, filters
from config import TOKEN
from handlers.start import start
from handlers.menu import show_menu
from handlers.help import help_command
from handlers.cancel import cancel
from handlers.order import start_order, choose_bread, choose_quantity, confirm_order

# Состояния
CHOOSING_BREAD = 1
CHOOSING_QUANTITY = 2
ORDER_CONFIRMATION = 3

app = Application.builder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start),
                  MessageHandler(filters.Regex("^Сделать заказ"), start_order)],
    states={
        CHOOSING_BREAD: [CallbackQueryHandler(choose_bread, pattern='^bread_')],
        CHOOSING_QUANTITY: [CallbackQueryHandler(choose_quantity, pattern='^\d$')],
        ORDER_CONFIRMATION: [CallbackQueryHandler(confirm_order, pattern='^confirm_order$')]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    allow_reentry=True
)

app.add_handler(conv_handler)
app.add_handler(MessageHandler(filters.Regex("^Меню"), show_menu))
app.add_handler(MessageHandler(filters.Regex("^Помощь"), help_command))

if __name__ == "__main__":
    app.run_polling()
