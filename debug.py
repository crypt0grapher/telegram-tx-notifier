import config
from messaging import send_telegram_message


def debugmsg(msg):
    if config.DEBUG:
        print(msg)
        send_telegram_message(msg)
