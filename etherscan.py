import requests
import time
import commands
from commands import ETHERSCAN_API_KEY
from debug import debugmsg
from helpers import safe_bignumber_to_float
from tg_interface import send_telegram_message
from collections import deque

transaction_cache = deque(maxlen=1000)
prev_data = {}


def get_etherscan_data(filter):
    global transaction_cache

    if not filter.active:
        return []
    # Get the latest block number first
    latest_block = get_blocknumber()

    # Looping through the addresses
    output_tx = []
    for address in filter.addresses:
        all_txs = get_tx_list_with_cache(address, latest_block - 5, latest_block)
        if not all_txs:
            continue
        if "result" in all_txs and isinstance(all_txs["result"], list):
            # filter by amount and address
            filtered_tx_by_amt_and_addr = [tx for tx in all_txs["result"] if
                                           tx["to" if filter.to_filter else "from"].lower() == address.lower() and
                                           filter.amount_from <= safe_bignumber_to_float(
                                               tx["value"]) <= filter.amount_to]
            # filter for fresh opoosite addresses
            filtered_tx_by_amt_and_addr_and_fresh = []
            if filter.fresh > 0:
                for tx in filtered_tx_by_amt_and_addr:
                    opposite_address = tx["to"] if tx["to"].lower() != address.lower() else tx["from"]
                    tx_count = get_tx_count(opposite_address)
                    if tx_count <= filter.fresh:
                        tx["tx_count"] = tx_count
                        filtered_tx_by_amt_and_addr_and_fresh.append(tx)
            else:
                filtered_tx_by_amt_and_addr_and_fresh = filtered_tx_by_amt_and_addr
            new_filtered_txs = [tx for tx in filtered_tx_by_amt_and_addr_and_fresh if
                                tx["hash"] not in transaction_cache]
            # Append new transaction hashes to the cache
            for tx in new_filtered_txs:
                transaction_cache.append(tx["hash"])
            debugmsg(
                "Filter: " + str(filter.name) +
                "Block " + str(latest_block) + ", Txs: " + str(len(all_txs)) + ", "
                "After filtering: " + str(len(new_filtered_txs)))
            output_tx.extend(new_filtered_txs)
    if len(output_tx) > 0:
        return output_tx
    else:
        debugmsg(
            "Filter: " + str(filter.name) +
            "Block " + str(latest_block) + ",Txs: " + str(len(all_txs)) + ", No new transactions found")
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


def get_blocknumber():
    url = "https://api.etherscan.io/api"
    parameters = {
        "module": "proxy",
        "action": "eth_blockNumber",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(url, params=parameters)
    data = response.json()
    if response.status_code == 200:
        return int(data["result"], 16)
    else:
        raise Exception(f"Error: {response.status_code} {response.text}")


def get_tx_list_with_cache(address, startblock, endblock):
    global prev_data
    url = "https://api.etherscan.io/api"
    parameters = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": startblock,
        "endblock": endblock,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(url, params=parameters)
    data = response.json()
    if response.status_code == 200:
        if prev_data.get(str(parameters)) == str(data):
            return []
        prev_data[str(parameters)] = str(data)
        return data
    else:
        raise Exception(f"Error: {response.status_code} {response.text}")


def get_tx_count(address):
    url = "https://api.etherscan.io/api"
    parameters = {
        "module": "proxy",
        "action": "eth_getTransactionCount",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(url, params=parameters)
    data = response.json()
    if response.status_code == 200:
        return int(data["result"], 16)
    else:
        raise Exception(f"Error: {response.status_code} {response.text}")


def get_request_with_throttling(params=None, **kwargs):
    url = "https://api.etherscan.io/api"
    time.sleep(commands.POLLING_SPEED)
    response = requests.get(url, params, **kwargs)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} {response.text}")
