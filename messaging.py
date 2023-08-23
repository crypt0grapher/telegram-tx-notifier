import requests
import telegram
import asyncio

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from config import ETHERSCAN_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, set_addresses, set_amount_from, \
    set_amount_to, display_config, toggle_debug, set_polling_speed

bot = telegram.Bot(TELEGRAM_BOT_TOKEN)

help_msg = "/config to view the current configuration.\n\
/adr to specify the sender addresses to monitor.\n\
/amt_from to set the minimum transaction amount to monitor.\n\
/amt_to to set the maximum transaction amount to monitor.\n\
/speed to define the polling frequency in seconds.\n\
/debug to toggle debug mode for detailed logging.\n\
/help to display this help message again."


def telegram_init():
    print(bot.get_me())
    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("adr", set_addresses, pass_args=True))
    dp.add_handler(CommandHandler("amt_from", set_amount_from, pass_args=True))
    dp.add_handler(CommandHandler("amt_to", set_amount_to, pass_args=True))
    dp.add_handler(CommandHandler("config", display_config, pass_args=True))
    dp.add_handler(CommandHandler("debug", toggle_debug, pass_args=False))
    dp.add_handler(CommandHandler("speed", set_polling_speed, pass_args=True))
    dp.add_handler(CommandHandler("help", help, pass_args=False))
    updater.start_polling()
    send_telegram_message("Ethereum Transaction Scanner Telegram Bot\n\n"+help_msg)
    return True


def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(help_msg)


def send_telegram_message(message):
    bot.send_message(text=message, chat_id=TELEGRAM_CHAT_ID, parse_mode="HTML")
