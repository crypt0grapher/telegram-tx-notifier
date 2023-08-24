import datetime
import sys
import time
import requests
import os

import commands
from etherscan import get_etherscan_data, etherscan_init
from helpers import safe_bignumber_to_float
from tg_interface import send_telegram_message, telegram_init
from dotenv import load_dotenv


def main():
    print("Telegram bot online")
    if not telegram_init():
        sys.exit("Error initializing telegram bot")
    if not etherscan_init():
        sys.exit("Error initializing etherscan")
    while True:
        if commands.BOT_IS_RUNNING:
            for address in commands.addresses:
                records = get_etherscan_data(address)
                current_message = ""
                for record in records:
                    amount = safe_bignumber_to_float(record["value"])
                    hash_with_link = f'<a href="https://etherscan.io/tx/{record["hash"]}">{record["hash"]}</a>'
                    dt_object = datetime.datetime.fromtimestamp(int(record[
                                                                        "timeStamp"]) if record[
                        "timeStamp"] else time.time())
                    print(dt_object.strftime('%Y-%m-%d %H:%M:%S'))
                    current_message = current_message + \
                                      "block: " + record["blockNumber"] + "\n" + \
                                      "timestamp: " + record["timeStamp"] + " (" + dt_object.strftime(
                        '%Y-%m-%d %H:%M:%S') + ")" + "\n" + \
                                      "gas price: " + record["gasPrice"] + "\n" + \
                                      "tx hash: " + hash_with_link + "\n" + \
                                      "from: " + record["from"] + "\n" + \
                                      "to: " + record["to"] + "\n" + \
                                      "value: " + str(amount) + " ETH\n\n"
                if current_message:
                    send_telegram_message(current_message)
        time.sleep(commands.POLLING_SPEED)  # Che
        # ck every second


if __name__ == "__main__":
    main()
