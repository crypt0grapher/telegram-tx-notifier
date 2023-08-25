import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext

from filter import Filter

load_dotenv()

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
DEBUG = False
POLLING_SPEED = 0.3
BOT_IS_RUNNING = False
FILTERS = []

addresses = ['0x56eddb7aa87536c09ccc2793473599fd21a8b17f']
amount_from = 0.01
amount_to = 10
uptime = 0


def add_filter(update: Update, context: CallbackContext) -> None:
    global FILTERS
    if len(context.args) == 0:
        update.message.reply_text("Please provide filter details, /help <code>addfilter</code> for more",
                                  parse_mode="HTML")
    else:
        try:
            filter_to_add = Filter(params_to_parse=' '.join(context.args))
            if filter_to_add in FILTERS:
                update.message.reply_text(f"Filter {filter_to_add}Already exists, skipping.")
            else:
                if any(f.name == filter_to_add.name for f in FILTERS):
                    raise ValueError(f"Filter with name {filter_to_add.name} already exists")
                FILTERS.append(filter_to_add)
                more_text = "\nBot is not running, please start it with /start" if not BOT_IS_RUNNING else ""
                update.message.reply_text(f"Filter created:\n{filter_to_add}{more_text}", parse_mode="HTML")
        except ValueError as e:
            update.message.reply_text(f"Error: {str(e)}")


def del_filter(update: Update, context: CallbackContext) -> None:
    global FILTERS
    if len(context.args) == 0:
        update.message.reply_text("Please provide filter name", parse_mode="HTML")
    else:
        try:
            filter_to_delete = None
            for filter in FILTERS:
                if filter.name.lower() == context.args[0].lower():
                    filter_to_delete = filter
                    break
            if filter_to_delete in FILTERS:
                FILTERS.remove(filter_to_delete)
                update.message.reply_text(f"Filter {filter_to_delete} deleted")
            else:
                update.message.reply_text(f"Filter {filter_to_delete} not found")
        except ValueError as e:
            update.message.reply_text(f"Error: {str(e)}")


def set_polling_speed(update: Update, context: CallbackContext) -> None:
    global POLLING_SPEED
    if len(context.args) == 0:
        update.message.reply_text("Please provide a number")
    else:
        POLLING_SPEED = int(context.args[0])
        if POLLING_SPEED < 0:
            update.message.reply_text(f"Polling speed must be greater than 0")
            POLLING_SPEED = 0
        elif POLLING_SPEED > 60:
            update.message.reply_text(f"Polling speed must be less than 60")
            POLLING_SPEED = 60
        else:
            update.message.reply_text(f"Polling speed set to: {POLLING_SPEED} seconds")


def toggle_debug(update: Update, context: CallbackContext) -> None:
    global DEBUG
    DEBUG = not DEBUG
    update.message.reply_text(f"Debug set to: {DEBUG}")


def display_config(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        f"<strong>Current bot configuration</strong>\n"
        f"Bot is {'off' if not BOT_IS_RUNNING else 'running'}\n"
        f"Filters: {len(FILTERS)}, active {sum(f.active for f in FILTERS)}\n"
        f"Etherscan is polled every {POLLING_SPEED} seconds\n",
        parse_mode="HTML")


def start_bot(update: Update, context: CallbackContext) -> None:
    global BOT_IS_RUNNING
    if len(FILTERS) > 0:
        BOT_IS_RUNNING = True
        update.message.reply_text("Bot started")
    else:
        update.message.reply_text("Please add at least one filter first")


def stop_bot(update: Update, context: CallbackContext) -> None:
    global BOT_IS_RUNNING
    BOT_IS_RUNNING = False
    update.message.reply_text("Bot stopped")


def filters(update: Update, context: CallbackContext) -> None:
    global FILTERS
    if len(FILTERS) == 0:
        update.message.reply_text("No active filters")
    else:
        update.message.reply_text(f"Active filters:\n{'<br/>'.join([str(f) for f in FILTERS])}", parse_mode="HTML")
