import requests

from config import ETHERSCAN_API_KEY


def get_etherscan_data(api_key, from_address, min_amount, max_amount):
    url = "https://api.etherscan.io/api"

    # Get the latest block number first
    latest_block_params = {
        "module": "proxy",
        "action": "eth_blockNumber",
        "apikey": api_key
    }
    response = requests.get(url, params=latest_block_params)
    latest_block = int(response.json()["result"], 16)

    # Adjust startblock to only retrieve recent transactions
    start_block = max(0, latest_block - 100)

    parameters = {
        "module": "account",
        "action": "txlist",
        "address": from_address,
        "startblock": start_block,
        "endblock": latest_block,
        "sort": "asc",
        "apikey": api_key
    }

    response = requests.get(url, params=parameters)
    data = response.json()

    # Filter transactions by 'From' address and amount
    return [tx for tx in data["result"] if
            tx["from"].lower() == from_address.lower() and min_amount <= float(tx["value"]) <= max_amount]



def etherscan_init():
    url = "https://api.etherscan.io/api"
    parameters = {
        "module": "proxy",
        "action": "eth_blockNumber",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(url, params=parameters)
    return response.status_code == 200