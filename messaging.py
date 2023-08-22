import requests
import telegram
import asyncio

from telegram.ext import Updater, CommandHandler
from telegram.utils.helpers import DEFAULT_NONE

from config import ETHERSCAN_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, set_addresses, set_amount_from, \
    set_amount_to, display_config, toggle_debug, set_polling_speed

bot = telegram.Bot(TELEGRAM_BOT_TOKEN)


def telegram_init():
    print(bot.get_me())
    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("set_addresses", set_addresses, pass_args=True))
    dp.add_handler(CommandHandler("set_amount_from", set_amount_from, pass_args=True))
    dp.add_handler(CommandHandler("set_amount_to", set_amount_to, pass_args=True))
    dp.add_handler(CommandHandler("display_config", display_config, pass_args=True))
    dp.add_handler(CommandHandler("debug", toggle_debug, pass_args=False))
    dp.add_handler(CommandHandler("set_polling_speed", set_polling_speed, pass_args=True))
    updater.start_polling()
    send_telegram_message("Bot online, use /display_config to see current configuration\n\
    Use /set_addresses to set sender addresses to watch\n\
    Use /set_amount_from to set minimum amount to watch\n\
    Use /set_amount_to to set maximum amount to watch\n\
    Use /set_polling_speed to set polling speed in seconds\n\
    Use /debug to toggle debug mode with extra logging")
    return True


def send_telegram_message(message, parse_mode=DEFAULT_NONE):
    bot.send_message(text=message, chat_id=TELEGRAM_CHAT_ID, parse_mode=parse_mode)
