import commands
from tg_interface import send_telegram_message


def debugmsg(msg):
    print(msg)
    if commands.DEBUG:
        send_telegram_message(msg)
