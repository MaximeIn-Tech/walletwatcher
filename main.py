import logging
import os
import socket

from dotenv import load_dotenv
from httpcore import ConnectError
from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, Updater

from menus import *
from messages import *

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="logs.log",
    encoding="utf-8",
    filemode="w",
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Import the token and connect to the bot
token = os.getenv("TELEGRAM_BOT_TOKEN")


############################ Keyboards #########################################


async def start(update, context):
    await update.message.reply_text(
        await main_menu_message(), reply_markup=await main_menu_keyboard()
    )


async def main_menu(update, context):
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=await main_menu_message(),
        reply_markup=await main_menu_keyboard(),
    )


async def add_wallet_menu(update, context):
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=await add_wallet_start_message(),
        reply_markup=await add_wallet_keyboard(),
    )


async def settings_menu(update, context):
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=await settings_message(),
        reply_markup=await settings_menu_keyboard(),
    )


async def language_selection_menu(update, context):
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=await language_selection_message(),
        reply_markup=await language_keyboard(),
    )


async def help(update, context):
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=await help_message(),
        reply_markup=await back_to_to_main_keyboard(),
    )


if __name__ == "__main__":
    print("Starting bot ...")
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(main_menu, pattern="main"))
    application.add_handler(
        CallbackQueryHandler(add_wallet_menu, pattern="add_wallet_menu")
    )
    application.add_handler(
        CallbackQueryHandler(settings_menu, pattern="settings_menu")
    )
    application.add_handler(CallbackQueryHandler(language_selection_menu))
    application.add_handler(CallbackQueryHandler(help, pattern="help_menu"))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

    try:
        print("Start polling ...")
        application.run_polling()
    except ConnectError as e:
        logging.error(f"Error while getting Updates: {e}")
    except socket.gaierror as e:
        logging.error(f"Error resolving hostname: {e}")
