import requests
import telegram
import asyncio

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from commands import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, display_config, toggle_debug, set_polling_speed, start_bot, \
    stop_bot, add_filter, filters, del_filter

bot = telegram.Bot(TELEGRAM_BOT_TOKEN)

help_msg = "/config to view the current configuration.\n\
/start to start the bot or a filter by number.\n\
/stop to stop the bot or a filter by number.\n\
/filters to view all the active filters.\n\
/addfilter to add a new filter, /help <code>addfilter</code> for more. \n\
/delfilter to delete a filter by name.\n\
/freq to set the polling frequency in seconds.\n\
/debug to toggle debug mode for detailed logging.\n\
/help to display this help message again."

addfilter_help_msg = "Add a new filter as a string ling in the following comma separated format:\n\
<code>from</code> space from addresses separated,\n\
<code>to</code> space separated receivers addresses, either <code>from</code> or <code>to</code> to be specified to set a filter,\n\
<code>fresh</code> max number of transactions to detect whether the counterpary address (reciever for 'from' filter and sender for 'to' filter) new, 0 to disable, default is 5 for from and 3 for to,\n\
<code>min</code> to set the minimum transaction amount ETH to monitor, default is 0\n\
<code>max</code> to set the maximum transaction amount ETH to monitor, default is 0.01.\n\
<code>name</code> human-readable filter name wihtous spaces, mandatory.\n\
Example:\n<code>/addfilter from</code> 0x56eddb7aa87536c09ccc2793473599fd21a8b17f, <code>fresh</code> 4, <code>min</code> 0, <code>max</code> 0.01, <code>name</code> Binance1 "


def telegram_init():
    print(bot.get_me())
    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("config", display_config, pass_args=True))
    dp.add_handler(CommandHandler("debug", toggle_debug, pass_args=False))
    dp.add_handler(CommandHandler("freq", set_polling_speed, pass_args=True))
    dp.add_handler(CommandHandler("help", help, pass_args=True))
    dp.add_handler(CommandHandler("start", start_bot, pass_args=True))
    dp.add_handler(CommandHandler("stop", stop_bot, pass_args=True))
    dp.add_handler(CommandHandler("addfilter", add_filter, pass_args=True))
    dp.add_handler(CommandHandler("delfilter", del_filter, pass_args=True))
    dp.add_handler(CommandHandler("filters", filters, pass_args=False))
    updater.start_polling()
    send_telegram_message("<strong>Ethereum Transaction Scanner Telegram Bot</strong>\n\n" + help_msg)
    return True


def help(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        update.message.reply_text(help_msg, parse_mode="HTML")
    elif context.args[0] == 'addfilter':
        update.message.reply_text(addfilter_help_msg, parse_mode="HTML")
    else:
        update.message.reply_text(
            "unrecognized argument, - it's either <code>/help</code> or <code>/help command_name</code>",
            parse_mode="HTML")


def send_telegram_message(message):
    bot.send_message(text=message, chat_id=TELEGRAM_CHAT_ID, parse_mode="HTML")
