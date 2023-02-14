import configparser
import redis
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
from utils import test
from chatbot import OpenAIBot
from log import logger

allowed_user_list = ["riverfjs", "victorwangkai"]
tt = OpenAIBot()
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # """Send a message when the command /help is issued."""
    await update.message.reply_text("你好, {}, 请选择左下角菜单开始使用！喵~".format(update.message.from_user["first_name"]))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Good day, {}!".format(context.args[0]))

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /chat is issued."""
    user = update.message.from_user
    if user["username"] not in allowed_user_list:
        await update.message.reply_text("对不起，不认识你！ 喵~ 不给用 喵~")
    else:
        try:
            keyword = context.args[0]
        except IndexError:
            await update.message.reply_text("请在命令后输入文字 /chat <keyword>，喵~")
        else:
            await update.message.reply_text(tt.reply(query=keyword, context={"user_id": user["username"], "type": "TEXT"}))

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /image is issued."""

    user = update.message.from_user
    if user["username"] not in allowed_user_list:
        await update.message.reply_text("对不起，不认识你！ 喵~ 不给用 喵~")
    else:
        try:
            keyword = context.args[0]
        except IndexError:
            await update.message.reply_text("请在命令后输入文字 /image <keyword>，喵~")
        else:
            await update.message.reply_photo(tt.reply(query=keyword, context={"user_id": user["username"], "type": "IMAGE_CREATE"}))

async def ytb(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /image is issued."""
    user = update.message.from_user
    if user["username"] not in allowed_user_list:
        await update.message.reply_text("对不起，不认识你！ 喵~ 不给用 喵~")
    else:
        try:
            keyword = context.args[0]
        except IndexError:
            await update.message.reply_text("请在命令后输入文字 /video <keyword>，喵~")
        else:
            await update.message.reply_text(test(keyword))

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logger.info(context.args[0])
        msg = context.args[0] # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        await update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        await update.message.reply_text('Usage: /add <keyword>')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

app = ApplicationBuilder().token(token=(config['TELEGRAM']['ACCESS_TOKEN'])).build()
redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']
['PASSWORD']), port=(config['REDIS']['REDISPORT']))

app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("chat", chat))
app.add_handler(CommandHandler("image", image))
app.add_handler(CommandHandler("video", ytb))

app.add_handler(CommandHandler("add", add))

# app.add_handler(CallbackQueryHandler(button))
# app.add_handler(CommandHandler("startchat", start_chat))
app.add_handler(MessageHandler(filters.TEXT &~filters.COMMAND, echo))
app.run_polling()