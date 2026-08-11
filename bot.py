import os
import re
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")
PORT = int(os.environ.get("PORT", "10000"))


def get_words(text: str):
    # split camelCase/PascalCase boundaries into spaces first
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
    return re.findall(r"[A-Za-z0-9]+", spaced)


def to_upper(t): return t.upper()
def to_lower(t): return t.lower()
def to_title(t): return " ".join(w.capitalize() for w in get_words(t))
def to_sentence(t):
    t = t.strip()
    return t[:1].upper() + t[1:].lower() if t else t
def to_camel(t):
    words = get_words(t)
    if not words:
        return t
    return words[0].lower() + "".join(w.capitalize() for w in words[1:])
def to_pascal(t): return "".join(w.capitalize() for w in get_words(t))
def to_snake(t): return "_".join(w.lower() for w in get_words(t))
def to_kebab(t): return "-".join(w.lower() for w in get_words(t))
def to_constant(t): return "_".join(w.upper() for w in get_words(t))
def to_alternating(t):
    return "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(t))

CASES = {
    "upper": ("🔠 UPPERCASE", to_upper),
    "lower": ("🔡 lowercase", to_lower),
    "title": ("🔤 Title Case", to_title),
    "sentence": ("📝 Sentence case", to_sentence),
    "camel": ("🐫 camelCase", to_camel),
    "pascal": ("🅿️ PascalCase", to_pascal),
    "snake": ("🐍 snake_case", to_snake),
    "kebab": ("🍢 kebab-case", to_kebab),
    "constant": ("🔒 CONSTANT_CASE", to_constant),
    "alt": ("🔀 aLtErNaTiNg", to_alternating),
}


def build_keyboard():
    keys = list(CASES.items())
    kb, row = [], []
    for key, (label, _) in keys:
        row.append(InlineKeyboardButton(label, callback_data=f"case|{key}"))
        if len(row) == 2:
            kb.append(row)
            row = []
    if row:
        kb.append(row)
    return InlineKeyboardMarkup(kb)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔁 Text Case Converter\n\n"
        "Just send me any text, then tap a button to convert it."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    context.user_data["text"] = text
    preview = text if len(text) <= 200 else text[:200] + "…"
    await update.message.reply_text(
        f"Text received:\n“{preview}”\n\nChoose a case:",
        reply_markup=build_keyboard(),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = context.user_data.get("text")
    if not text:
        await query.edit_message_text("⚠️ Send me some text first, then tap a case.")
        return

    key = query.data.split("|", 1)[1]
    label, func = CASES[key]
    result = func(text)

    await query.edit_message_text(
        f"{label}\n\n{result}",
        reply_markup=build_keyboard(),
    )


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    if RENDER_EXTERNAL_URL:
        webhook_path = BOT_TOKEN
        webhook_url = f"{RENDER_EXTERNAL_URL}/{webhook_path}"
        logger.info("Starting webhook at %s", webhook_url)
        application.run_webhook(
            listen="0.0.0.0", port=PORT, url_path=webhook_path, webhook_url=webhook_url,
        )
    else:
        logger.info("RENDER_EXTERNAL_URL not set - polling mode (local dev)")
        application.run_polling()


if __name__ == "__main__":
    main()
