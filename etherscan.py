import requests

import config
from config import ETHERSCAN_API_KEY
from debug import debugmsg
from helpers import safe_bignumber_to_float
from messaging import send_telegram_message

prev_block_response = ""


def get_etherscan_data(address):
    global prev_block_response
    from_address = address
    min_amount = config.amount_from
    max_amount = config.amount_to
    url = "https://api.etherscan.io/api"

    # Get the latest block number first
    latest_block_params = {
        "module": "proxy",
        "action": "eth_blockNumber",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(url, params=latest_block_params)
    latest_block = int(response.json()["result"], 16)

    parameters = {
        "module": "account",
        "action": "txlist",
        "address": from_address,
        "startblock": latest_block,
        "endblock": latest_block,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }

    response = requests.get(url, params=parameters)
    data = response.json()
    if prev_block_response == data:
        return []
    prev_block_response = data
    print(data)
    if isinstance(data["result"], list):
        filtered_tx = [tx for tx in data["result"] if
                       tx["from"].lower() == from_address.lower() and min_amount <= safe_bignumber_to_float(
                           tx["value"]) <= max_amount]
        debugmsg(
            "Block " + str(latest_block) + "\nTxs: " + str(
                len(data["result"])) + "\nAfter filtering: " + str(len(filtered_tx)))
        return filtered_tx
    else:
        debugmsg(f"block: {latest_block}, no transactions found: {data}")
        return []


def etherscan_init():
    url = "https://api.etherscan.io/api"
    parameters = {
        "module": "proxy",
        "action": "eth_blockNumber",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(url, params=parameters)
    return response.status_code == 200
