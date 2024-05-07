import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


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

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# TODO : Function to check the token symbol and interact depending on that with multiple different calls.

######################################## ETH BLOCKCHAIN ############################################

ethapikey = os.getenv("ETH_API_KEY")


def fetch_eth_balance_multiple_addresses(wallet_addresses):
    url = f"https://api.bscscan.com/api?module=account&action=balancemulti&address={wallet_addresses}&tag=latest&apikey={ethapikey}"

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


def fetch_eth_single_wallet_balance(wallet_addresse, contract_address):

    url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={contract_address}&address={wallet_addresse}&tag=latest&apikey={ethapikey}"

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

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def fetch_bnb_balance_multiple_addresses(wallet_addresses):
    url = f"https://api.etherscan.io/api?module=account&action=balancemulti&address={wallet_addresses}&tag=latest&apikey={bscapikey}"

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


# TODO : Function to check the token symbol and interact depending on that with multiple different calls.

######################################## OVERALL CHECK #############################################
# def fetch_wallet_balance(blockchain, wallet_address, contract_address):
#     if blockchain == "THETA":
