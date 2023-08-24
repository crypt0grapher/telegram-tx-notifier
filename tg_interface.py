import requests
import telegram
import asyncio

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from commands import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, set_addresses, \
    set_amount_from, \
    set_amount_to, display_config, toggle_debug, set_polling_speed, start_bot, stop_bot, add_filter, filters

bot = telegram.Bot(TELEGRAM_BOT_TOKEN)

help_msg = "/config to view the current configuration.\n\
/start to start the bot.\n\
/stop to stop the bot.\n\
/filters to view all the active filters.\n\
/addfilter to add a new filter as a string ling in the following comma separated format: \n\
    <code>from</code> space from addresses separated,\n\
    <code>to</code> space separated receivers addresses (can be blank but not both),\n\
    <code>fresh_from</code> max number of transactions to detect whether the address is new, 0 to disable, default is 5,\n\
    <code>fresh_to</code> same for <b>to</b> address, 3 is default, 0 means freshness is not being checked, \n\
    <code>amt_from</code> to set the minimum transaction amount ETH to monitor, default is 0\n\
    <code>amt_to</code> to set the maximum transaction amount ETH to monitor, default is 0.01.\n\
/delfilter N to delete a filter number N.\n\
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
    dp.add_handler(CommandHandler("start", start_bot, pass_args=False))
    dp.add_handler(CommandHandler("stop", stop_bot, pass_args=False))
    dp.add_handler(CommandHandler("addfilter", add_filter, pass_args=True))
    dp.add_handler(CommandHandler("filters", filters, pass_args=False))
    updater.start_polling()
    send_telegram_message("<strong>Ethereum Transaction Scanner Telegram Bot</strong>\n\n" + help_msg)
    return True


def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(help_msg, parse_mode="HTML")

def send_telegram_message(message):
    bot.send_message(text=message, chat_id=TELEGRAM_CHAT_ID, parse_mode="HTML")
