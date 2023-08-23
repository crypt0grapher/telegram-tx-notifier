import requests

import config
from config import ETHERSCAN_API_KEY
from debug import debugmsg
from helpers import safe_bignumber_to_float
from messaging import send_telegram_message
from collections import deque

transaction_cache = deque(maxlen=1000)
prev_data = ""


def get_etherscan_data(address):
    global prev_data
    global transaction_cache
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
        "startblock": latest_block - 5,
        "endblock": latest_block,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }

    response = requests.get(url, params=parameters)
    data = response.json()
    if prev_data == data:
        return []
    prev_data = data

    print(data)
    if "result" in data and isinstance(data["result"], list):
        filtered_tx = [tx for tx in data["result"] if
                       tx["from"].lower() == from_address.lower() and min_amount <= safe_bignumber_to_float(
                           tx["value"]) <= max_amount]
        new_filtered_txs = [tx for tx in filtered_tx if tx["hash"] not in transaction_cache]
        # Append new transaction hashes to the cache
        for tx in new_filtered_txs:
            transaction_cache.append(tx["hash"])
        debugmsg(
            "Block " + str(latest_block) + "\nTxs: " + str(
                len(data["result"])) + "\nAfter filtering: " + str(len(new_filtered_txs)))
        return new_filtered_txs
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
