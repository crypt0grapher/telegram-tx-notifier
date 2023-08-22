import sys
import time
import requests
import os

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

    # while True:
    #     records = get_etherscan_data("HDECNPE6FDK593ASIA2UTIWQPHY4F4H4QV", "0x82ff5530b1c1766cf2c310af55831c1279622daa",
    #                                  0, 99999999999999999999)
    #
    #     if not last_record:
    #         last_record = records[-1]
    #     elif records[-1] != last_record:
    #         send_telegram_notification(
    #             "6569907923:AAENQCY5Tr3e8FEADTMKjWR2laH6D2Mhslk",
    #             "@EthereumEventsNotifierBot",
    #             "A new record has been detected in Etherscan based on your filter."
    #         )
    #         last_record = records[-1]
    #
    #     time.sleep(1)  # Check every second


if __name__ == "__main__":
    main()
