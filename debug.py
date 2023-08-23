import config
from messaging import send_telegram_message


def debugmsg(msg):
    print(msg)
    if config.DEBUG:
        send_telegram_message(msg)
