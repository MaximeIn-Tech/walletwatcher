import json
import os

import requests
from dotenv import load_dotenv

from database import fetch_decimal_for_contract

load_dotenv()

ethapikey = os.getenv("ETH_API°KEY")
bscapikey = os.getenv("BSC_API°KEY")

###################################### THETA BLOCKCHAIN ############################################
# TODO: Limiter les calls pour Thetascan à 2 par secondes


def fetch_data_contract(contract_address):
    url = f"https://www.thetascan.io/api/contract/?contract={contract_address}"
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def fetch_theta_single_wallet_balance(wallet_address, contract_address):
    url = f"http://www.thetascan.io/api/contract/?contract={contract_address}&address={wallet_address}"

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            balance = data["balance"]
            return balance

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def fetch_theta_balance(wallet_address):
    url = f"http://www.thetascan.io/api/balance/?address={wallet_address}"

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            theta_balance = data["theta"]

            return theta_balance

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def fetch_tfuel_balance(wallet_address):
    url = f"http://www.thetascan.io/api/balance/?address={wallet_address}"

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            tfuel_balance = data["tfuel"]

            return tfuel_balance

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def fetch_theta_stake(wallet_address):
    url = f"https://explorer-api.thetatoken.org/api/stake/{wallet_address}?types[]=vcp&types[]=gcp&types[]=eenp"

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            return data

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# TODO : Function to check the token symbol and interact depending on that with multiple different calls.

######################################## ETH BLOCKCHAIN ############################################

ethapikey = os.getenv("ETH_API_KEY")


def fetch_eth_token_balance(wallet_address):
    url = f"https://api.etherscan.com/api?module=account&action=balance&address={wallet_address}&apikey={ethapikey}"

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            balance = data["result"]
            balance = int(balance) * (10**-18)

            return balance

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# def fetch_eth_token_balance_multiple_addresses(wallet_addresses):
#     url = f"https://api.bscscan.com/api?module=account&action=balancemulti&address={wallet_addresses}&tag=latest&apikey={ethapikey}"

#     try:
#         # Send a GET request to the URL
#         response = requests.get(url)

#         # Check if the request was successful (status code 200)
#         if response.status_code == 200:
#             data = response.json()

#         else:
#             print(f"Failed to retrieve data. Status code: {response.status_code}")
#             return None
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None


def fetch_eth_single_wallet_balance(wallet_addresse, contract_address):

    url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={contract_address}&address={wallet_addresse}&tag=latest&apikey={ethapikey}"

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            balance = data["result"]

            return balance

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# TODO : Function to check the token symbol and interact depending on that with multiple different calls.

######################################## BSC BLOCKCHAIN ############################################

bscapikey = os.getenv("BSC_API_KEY")


def fetch_bsc_single_wallet_balance(wallet_addresse, contract_address):
    url = f"https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={contract_address}&address={wallet_addresse}&tag=latest&apikey={bscapikey}"

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            balance = data["result"]

            return balance

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# def fetch_bnb_token_balance_multiple_addresses(wallet_addresses):
#     url = f"https://api.etherscan.io/api?module=account&action=balancemulti&address={wallet_addresses}&tag=latest&apikey={bscapikey}"

#     try:
#         # Send a GET request to the URL
#         response = requests.get(url)

#         # Check if the request was successful (status code 200)
#         if response.status_code == 200:
#             data = response.json()

#         else:
#             print(f"Failed to retrieve data. Status code: {response.status_code}")
#             return None
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None


def fetch_bnb_token_balance(wallet_address):
    url = f"https://api.bscscan.com/api?module=account&action=balance&address={wallet_address}&apikey={bscapikey}"

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            balance = data["result"]
            balance = int(balance) * (10**-18)

            return balance

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# TODO : Function to check the token symbol and interact depending on that with multiple different calls.


######################################## OVERALL CHECK #############################################
def fetch_wallet_balance(blockchain, token_symbol, wallet_address, contract_address):
    if blockchain == "THETA":
        if token_symbol == "THETA":
            balance = fetch_theta_balance(wallet_address)
            return balance
        elif token_symbol == "TFUEL":
            balance = fetch_tfuel_balance(wallet_address)
            return balance
        else:
            fetch_theta_single_wallet_balance(wallet_address, contract_address)
    elif blockchain == "ETH":
        if token_symbol == "ETH":
            balance = fetch_eth_token_balance(wallet_address)
            return balance
        else:
            decimal = fetch_decimal_for_contract("ETH", contract_address)
            balance = fetch_eth_single_wallet_balance(wallet_address, contract_address)
            balance = int(balance) * (10**-decimal)
            return balance
    elif blockchain == "BSC":
        if token_symbol == "BNB":
            balance = fetch_bnb_token_balance(wallet_address)
            return balance
        else:
            decimal = fetch_decimal_for_contract("BSC", contract_address)
            balance = fetch_bsc_single_wallet_balance(wallet_address, contract_address)
            balance = int(balance) * (10**-decimal)
            return balance


def main():
    data = fetch_theta_stake("0xCB2A9C1336C6CB83BF5453791138ED350C343BC5")
    print(data)


if __name__ == "__main__":
    main()
