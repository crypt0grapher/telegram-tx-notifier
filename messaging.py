import requests
import telegram
import asyncio

from config import ETHERSCAN_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

bot = telegram.Bot(TELEGRAM_BOT_TOKEN)


def telegram_init():
    print(bot.get_me())
    send_telegram_message("Bot online")
    return True


def send_telegram_message(message):
    bot.send_message(text=message, chat_id=TELEGRAM_CHAT_ID)
