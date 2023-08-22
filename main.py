import sys
import time
import requests
import os

import config
from etherscan import get_etherscan_data, etherscan_init
from messaging import send_telegram_message, telegram_init
from dotenv import load_dotenv


def main():
    print("Telegram bot online")
    if not telegram_init():
        sys.exit("Error initializing telegram bot")
    if not etherscan_init():
        sys.exit("Error initializing etherscan")

    last_record = None

    while True:
        if config.DEBUG:
            send_telegram_message("Checking for new transactions...")
        for address in config.addresses:
            if config.DEBUG:
                send_telegram_message(f"Qurying Etherscan for sender {address}")
            records = get_etherscan_data(address)
            if records and last_record != records[-1]:
                send_telegram_message(
                    "tx hash: " + records[-1]["hash"] + "\n" + "from: " + records[-1]["from"] + "\n" + "to: "
                    + records[-1]["to"] + "\n" + "value: " + records[-1]["value"]
                )
                message = f'<a href="https://etherscan.io/tx/{records[-1]["hash"]}">View Transaction on Etherscan</a>'
                send_telegram_message(message, parse_mode="HTML")

                last_record = records[-1]

        time.sleep(config.POLLING_SPEED)  # Check every second


if __name__ == "__main__":
    main()
