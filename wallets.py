import asyncio
import json
import os
import time

import aiohttp
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from database import fetch_decimal_for_contract

load_dotenv()

# Alchemy API Key
ALCHEMY_API_KEY = os.getenv("SOL_API_KEY")
ALCHEMY_URL = f"https://solana-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"


def fetch_data_contract(blockchain, contract_address):
    # Set up Selenium WebDriver for headless operation (no UI)
    options = Options()
    # options.add_argument("--headless")  # Run in headless mode (without UI)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    if blockchain == "THETA":
        url = f"https://www.thetascan.io/api/contract/?contract={contract_address}"
        try:
            # Fetch data using an API (no need for Selenium)
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                symbol = data["symbol"]
                decimal = data["decimal"]
                return symbol, decimal
            else:
                print(f"Failed to retrieve data. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    elif blockchain == "TON":
        url = f"https://tonapi.io/v2/jettons/{contract_address}"
        try:
            # Fetch data using an API (no need for Selenium)
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                symbol = data["metadata"]["symbol"]
                decimal = data["metadata"]["decimals"]
                return symbol, decimal
            else:
                print(f"Failed to retrieve data. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    elif blockchain == "BSC":
        url = f"https://bscscan.com/token/{contract_address}"
        driver.get(url)
        time.sleep(5)  # Allow time for page to load

        try:
            muted_element = driver.find_element(
                By.XPATH,
                "//span[@class='fs-base fw-medium']//span[@class='text-muted']",
            )
            symbol = muted_element.text.strip("()")
            decimal_element = driver.find_element(
                By.XPATH, "//h4[@class='text-cap mb-1']/b"
            )
            decimal = decimal_element.text
        except Exception as e:
            print(f"Error extracting BSC data: {e}")
            return None
        finally:
            driver.quit()

        return symbol, decimal

    elif blockchain == "ETH":
        url = f"https://etherscan.io/token/{contract_address}"
        driver.get(url)
        time.sleep(5)  # Allow time for page to load

        try:
            decimal_value = driver.find_element(
                By.CSS_SELECTOR, "h4.text-cap.mb-1 b"
            ).text
        except Exception:
            decimal_value = "N/A"  # Handle missing element

        try:
            token_symbol = driver.find_element(
                By.CSS_SELECTOR, "span.fs-base.fw-medium span.text-muted"
            ).text
            token_symbol = token_symbol.replace("(", "").replace(")", "")
        except Exception:
            token_symbol = "N/A"  # Handle missing element

        driver.quit()
        return token_symbol, decimal_value

    if blockchain == "SOL":
        url = f"https://solscan.io/token/{contract_address}"
        driver.get(url)

        # Wait for the page to load and ensure necessary elements are available
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "div.not-italic.font-normal.text-neutral7.text-\\[14px\\].leading-\\[24px\\].autoTruncate.block",
                    )
                )
            )

            token_name_element = driver.find_element(
                By.CSS_SELECTOR,
                "div.not-italic.font-normal.text-neutral7.text-\\[14px\\].leading-\\[24px\\].autoTruncate.block",
            )
            token_name = token_name_element.text
            token_symbol = "N/A"
            if "(" in token_name and ")" in token_name:
                token_symbol = token_name.split("(")[1].split(")")[0]

        except Exception as e:
            token_symbol = "N/A"
            decimal = "N/A"
            print(f"Error in extracting token name or decimal: {e}")

        try:
            url = ALCHEMY_URL
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTokenSupply",
                "params": [contract_address],  # Doit être une liste
            }
            headers = {"Content-Type": "application/json"}

            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            decimal = data["result"]["value"]["decimals"]
            return token_symbol, decimal
        except Exception as e:
            print(f"Error fetching balance: {e}")

        driver.quit()

    return None


###################################### THETA BLOCKCHAIN ############################################
# TODO: Limiter les calls pour Thetascan à 2 par secondes


def fetch_theta_single_wallet_balance(wallet_address, contract_address):
    url = f"http://www.thetascan.io/api/contract/?contract={contract_address}&address={wallet_address}"

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            balance = data
            return balance["balance"]
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

######################################## SOL BLOCKCHAIN ############################################


def fetch_sol_token_balance(wallet_address):
    url = f"{ALCHEMY_URL}"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [wallet_address],
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()
        balance_lamports = data["result"]["value"]
        balance_sol = balance_lamports / 1e9  # Convert lamports to SOL
        return balance_sol
    except Exception as e:
        return f"Error: {e}"


def fetch_sol_single_wallet_balance(wallet_address, contract_address):
    url = f"{ALCHEMY_URL}"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenAccountsByOwner",
        "params": [
            wallet_address,
            {"mint": contract_address},
            {"encoding": "jsonParsed"},
        ],
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        if data["result"]["value"]:
            # Assuming the first account contains the token balance
            token_account = data["result"]["value"][0]
            balance = token_account["account"]["data"]["parsed"]["info"]["tokenAmount"][
                "uiAmount"
            ]
            return balance
        else:
            balance = 0  # Set balance to 0 if no tokens are found
            return balance
    except Exception as e:
        return f"Error: {e}"


######################################## TON BLOCKCHAIN ############################################
def fetch_ton_token_balance(wallet_address: str) -> float:
    url = f"https://tonapi.io/v2/accounts/{wallet_address}"
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            balance = data["balance"]
            balance = balance / 10e8

            return balance

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def fetch_ton_single_wallet_balance(
    wallet_address: str, contract_address: str
) -> float:
    url = f"https://tonapi.io/v2/accounts/{wallet_address}/jettons/{contract_address}"
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            balance = int(data["balance"])
            decimal = int(data["jetton"]["decimals"])
            balance = balance / 10**decimal

            return balance

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


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
            balance = fetch_theta_single_wallet_balance(
                wallet_address, contract_address
            )
            balance = float(balance)
            return balance
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
    elif blockchain == "SOL":
        if token_symbol == "SOL":
            balance = fetch_sol_token_balance(wallet_address)
            return balance
        else:
            balance = fetch_sol_single_wallet_balance(wallet_address, contract_address)
            return balance
    elif blockchain == "TON":
        if token_symbol == "TON":
            balance = fetch_ton_token_balance(wallet_address)
            return balance
        else:
            balance = fetch_ton_single_wallet_balance(wallet_address, contract_address)
            return balance


async def main():
    # balance_ton = fetch_ton_token_balance(
    #     "UQCMOXxD-f8LSWWbXQowKxqTr3zMY-X1wMTyWp3B-LR6syif"
    # )
    # print(f"{balance_ton:,}")
    # data_single_token = fetch_ton_single_wallet_balance(
    #     "UQCMOXxD-f8LSWWbXQowKxqTr3zMY-X1wMTyWp3B-LR6syif",
    #     "EQD5ty5IxV3HECEY1bbbdd7rNNY-ZcA-pAIGQXyyRZRED9v3",
    # )
    # print(data_single_token)
    # balance = fetch_sol_single_wallet_balance(
    #     "6EnmSaKXCBRQ4NH4i2AqGnDscR52bRSn73BGvnKuf5Ji",
    #     "M5MFPbS4X6eYek21xhFU38DTavMLuGY9eyC5p8Tpump",
    # )
    # print(balance)
    # symbol, decimal = fetch_data_contract(
    #     "ETH", "0xf34960d9d60be18cC1D5Afc1A6F012A723a28811"
    # )
    # print("ETH---")
    # print(symbol)
    # print(decimal)
    # symbol, decimal = fetch_data_contract(
    #     "THETA", "0x645d521871406d97c36a0aed07c7a88d08095d35"
    # )
    # print("THETA---")
    # print(symbol)
    # print(decimal)
    # symbol, decimal = fetch_data_contract(
    #     "TON", "EQDWSm618mrf84PUjlu8rAMnlTa3RGhMzWb-UadvB5vLyqCv"
    # )
    # print("TON---")
    # print(symbol)
    # print(decimal)
    symbol, decimal = fetch_data_contract(
        "SOL", "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm"
    )
    print("SOL---")
    print(symbol)
    print(decimal)
    # symbol, decimal = fetch_data_contract(
    #     "BSC", "0x352Cb5E19b12FC216548a2677bD0fce83BaE434B"
    # )
    # print("BSC---")
    # print(symbol)
    # print(decimal)


if __name__ == "__main__":
    asyncio.run(main())
