import configparser
import redis
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
from log import logger

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # """Send a message when the command /help is issued."""
    await update.message.reply_text("你好, {}".format(update.message.from_user["first_name"]))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Good day, {}!".format(context.args[0]))


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logger.info(context.args[0])
        msg = context.args[0]  # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        await update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        await update.message.reply_text('Usage: /add <keyword>')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

app = ApplicationBuilder().token(
    token=(config['TELEGRAM']['ACCESS_TOKEN'])).build()
redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']
                                                               ['PASSWORD']), port=(config['REDIS']['REDISPORT']))

app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("add", add))

# app.add_handler(CallbackQueryHandler(button))
# app.add_handler(CommandHandler("startchat", start_chat))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
# app.run_polling()
app.run_webhook(
    listen="0.0.0.0",
    port=8000,
    webhook_url="https://comp7940.azurewebsites.net/"
)
