from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, CallbackQueryHandler, filters
from config import TOKEN
from handlers.start import start
from handlers.menu import show_menu
from handlers.help import help_command
from handlers.cancel import cancel

app = Application.builder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        0: [
            MessageHandler(filters.Regex("^Сделать заказ"), start),
            MessageHandler(filters.Regex("^Меню"), show_menu),
            MessageHandler(filters.Regex("^Помощь"), help_command),
        ]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    allow_reentry=True
)

app.add_handler(conv_handler)

if __name__ == "__main__":
    app.run_polling()
