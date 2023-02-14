import configparser
from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import ApplicationBuilder, Application, CommandHandler, ContextTypes, MessageHandler, filters


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

config = configparser.ConfigParser()
config.read('config.ini')

app = ApplicationBuilder().token(token=(config['TELEGRAM']['ACCESS_TOKEN'])).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()