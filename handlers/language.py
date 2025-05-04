from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from keyboards.main_keyboard import get_main_keyboard

# Промежуточное хранилище языков по user_id
user_languages = {}

def get_language_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")
        ],
        [
            InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
        ]
    ])

async def choose_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выберите язык / Elige idioma / Sprache wählen / Choose a language:",
        reply_markup=get_language_keyboard()
    )

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    lang_map = {
        "lang_ru": ("ru", "Язык установлен: Русский 🇷🇺"),
        "lang_es": ("es", "Idioma establecido: Español 🇪🇸"),
        "lang_de": ("de", "Sprache eingestellt: Deutsch 🇩🇪"),
        "lang_en": ("en", "Language set to: English 🇬🇧")
    }

    if data not in lang_map:
        return

    lang_code, confirmation_text = lang_map[data]
    user_id = query.from_user.id
    user_languages[user_id] = lang_code

    await query.edit_message_text(confirmation_text)
    await query.message.reply_text(
        "Главное меню обновлено:",
        reply_markup=get_main_keyboard(lang_code)
    )
