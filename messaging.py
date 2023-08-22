import requests
import telegram
import asyncio

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from config import ETHERSCAN_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, set_addresses, set_amount_from, \
    set_amount_to, display_config, toggle_debug, set_polling_speed

bot = telegram.Bot(TELEGRAM_BOT_TOKEN)

help_msg = "Use /config to see current configuration\n\
    Use /adr to set sender addresses to watch\n\
    Use /amt_from to set minimum amount to watch\n\
    Use /amt_to to set maximum amount to watch\n\
    Use /speed to set polling speed in seconds\n\
    Use /debug to toggle debug mode with extra logging\n\
    Use /help to see this message again"


def telegram_init():
    print(bot.get_me())
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("adr", set_addresses, pass_args=True))
    dp.add_handler(CommandHandler("amt_from", set_amount_from, pass_args=True))
    dp.add_handler(CommandHandler("amt_to", set_amount_to, pass_args=True))
    dp.add_handler(CommandHandler("config", display_config, pass_args=True))
    dp.add_handler(CommandHandler("debug", toggle_debug, pass_args=False))
    dp.add_handler(CommandHandler("speed", set_polling_speed, pass_args=True))
    dp.add_handler(CommandHandler("help", help, pass_args=False))
    updater.start_polling()
    send_telegram_message("Telegram bot online")
    send_telegram_message(help_msg)
    return True


def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(help_msg)


def send_telegram_message(message):
    bot.send_message(text=message, chat_id=TELEGRAM_CHAT_ID, parse_mode="HTML")
