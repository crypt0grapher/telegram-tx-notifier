import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext

load_dotenv()

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
DEBUG = False;
POLLING_SPEED = int(os.getenv('POLLING_SPEED'))

addresses = ['0x28C6c06298d514Db089934071355E5743bf21d60']
amount_from = 0
amount_to = 100


def set_addresses(update: Update, context: CallbackContext) -> None:
    global addresses
    args = context.args
    addresses = args
    if len(addresses) == 0:
        update.message.reply_text("Please provide at least one address, or more separated by spaces")
    else:
        update.message.reply_text(f"Addresses set to: {', '.join(addresses)}")


def set_amount_from(update: Update, context: CallbackContext) -> None:
    global amount_from
    if len(context.args) == 0:
        update.message.reply_text("Please provide a number")
    elif len(context.args) > 1:
        update.message.reply_text("Please provide only one number")
    else:
        amount_from = float(context.args[0])
        if amount_from > amount_to:
            update.message.reply_text(f"Amount from must be less than amount to")
            amount_from = amount_to
        elif amount_from < 0:
            update.message.reply_text(f"Amount from must be greater than 0")
            amount_from = 0
        elif amount_from > 999999:
            update.message.reply_text(f"Amount from must be less than 999999")
            amount_from = 999999
        else:
            update.message.reply_text(f"Amount from set to: {amount_from}")


def set_amount_to(update: Update, context: CallbackContext) -> None:
    global amount_to
    if len(context.args) == 0:
        update.message.reply_text("Please provide a number")
    elif len(context.args) > 1:
        update.message.reply_text("Please provide only one number")
    else:
        amount_to = float(context.args[0])
        if context.args[0] == "":
            update.message.reply_text("Please provide a number")
        elif amount_to < amount_from:
            update.message.reply_text(f"Amount to must be greater than amount from")
            amount_to = amount_from
        elif amount_to < 0:
            update.message.reply_text(f"Amount to must be greater than 0")
            amount_to = 0
        elif amount_to > 999999:
            update.message.reply_text(f"Amount to must be less than 999999")
            amount_to = 999999
        else:
            update.message.reply_text(f"Amount to set to: {amount_to}")


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
        f"Current bot configuration\nAddresses: {', '.join(addresses)}\nAmount from: {amount_from}\nAmount to: {amount_to}\nPolling speed: {POLLING_SPEED} seconds\nDebug: {DEBUG}")
