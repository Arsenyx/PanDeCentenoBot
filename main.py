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

# ConversationHandler
conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start),  # Обработчик для команды /start
        CallbackQueryHandler(start_order, pattern="^make_order$")  # Обработчик для inline-кнопки "Сделать заказ"
    ],
    states={
        CHOOSING_BREAD: [CallbackQueryHandler(choose_bread, pattern="^bread_")],  # Выбор хлеба
        CHOOSING_QUANTITY: [CallbackQueryHandler(choose_quantity, pattern="^\d$")],  # Выбор количества
        ORDER_CONFIRMATION: [CallbackQueryHandler(confirm_order, pattern="^confirm_order$")]  # Подтверждение заказа
    },
    fallbacks=[CommandHandler("cancel", cancel)],  # Отмена заказа
    allow_reentry=True  # Разрешение на повторное подключение
)

# Добавляем обработчики
app.add_handler(conv_handler)
app.add_handler(MessageHandler(filters.Regex("^Меню$"), show_menu))  # Обработчик для кнопки "Меню"
app.add_handler(MessageHandler(filters.Regex("^Помощь$"), help_command))  # Обработчик для кнопки "Помощь"

if __name__ == "__main__":
    app.run_polling()
