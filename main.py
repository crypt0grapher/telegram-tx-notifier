import datetime
import sys
import time
import requests
import os

import config
from etherscan import get_etherscan_data, etherscan_init
from helpers import safe_bignumber_to_float
from messaging import send_telegram_message, telegram_init
from dotenv import load_dotenv


def main():
    print("Telegram bot online")
    if not telegram_init():
        sys.exit("Error initializing telegram bot")
    if not etherscan_init():
        sys.exit("Error initializing etherscan")

    while True:
        for address in config.addresses:
            records = get_etherscan_data(address)
            for record in records:
                amount = safe_bignumber_to_float(record["value"])
                hash_with_link = f'<a href="https://etherscan.io/tx/{record["hash"]}">{record["hash"]}</a>'
                dt_object = datetime.datetime.fromtimestamp(int(record[
                        "timeStamp"]) if record["timeStamp"] else time.time())
                print(dt_object.strftime('%Y-%m-%d %H:%M:%S'))
                send_telegram_message(
                    "block: " + record["blockNumber"] + "\n" + "timestamp: " + record[
                        "timeStamp"] + " ("+dt_object.strftime('%Y-%m-%d %H:%M:%S')+")" + "\n" + "gas price: " + record["gasPrice"] + "\n" +
                    "tx hash: " + hash_with_link + "\n" + "from: " + record["from"] + "\n" + "to: "
                    + record["to"] + "\n" + "value: " + str(amount) + " ETH\n"
                )
            time.sleep(config.POLLING_SPEED)  # Check every second


if __name__ == "__main__":
    main()
