"""
NOTE : This file is here to handle all the database interaction.
"""

import json
import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

# Configure logger
logger = logging.getLogger(__name__)

# Create a TimedRotatingFileHandler with date in filename
handler = TimedRotatingFileHandler(
    time.strftime("logs/database/database_log-%Y-%m-%d.log"),
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8",
)

# Formatter for the log messages
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Apply formatter to the handler
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# Set the log level
logger.setLevel(logging.INFO)

# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

# Example of logging
logger.info("Logging setup complete.")


def connect_to_database():
    """
    Connects to the Supabase database.

    Returns:
        Client: Supabase client object for interacting with the database.
    """
    load_dotenv()
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)


async def get_language_for_chat_id(chat_id):
    supabase = connect_to_database()
    try:
        # Query the Users table for the language with the specified chat_id
        user_response = (
            supabase.table("Users")
            .select("language")
            .eq("chat_id", chat_id)
            .limit(1)  # Limit to one result since chat_id should be unique
            .execute()
        )

        # If there is data for the specified chat_id, return the language
        if user_response.data:
            language = user_response.data
            language = language[0]["language"]
            return language
            return None  # Return None if no data found for the chat_id
    except Exception as e:
        logger.info("An error occurred while fetching user's language:", e)
        return None  # Return None in case of any errors


async def fetch_wallets_user(chat_id):
    supabase = connect_to_database()
    try:
        wallet_number = (
            supabase.table("Wallets")
            .select("*", count="exact")
            .eq("chat_id", chat_id)
            .execute()
        )

        if wallet_number:
            return wallet_number
            return None  # Return None if no data found for the chat_id
    except Exception as e:
        logger.info("An error occurred while fetching user's wallets:", e)
        return None  # Return None in case of any errors


async def fetch_wallet_address(wallet_address):
    supabase = connect_to_database()
    try:
        wallet_number = (
            supabase.table("Wallets")
            .select("*", count="exact")
            .eq("wallet_address", wallet_address)
            .execute()
        )

        if wallet_number:
            return wallet_number
            return None  # Return None if no data found for the chat_id
    except Exception as e:
        logger.info("An error occurred while fetching user's wallet addresses:", e)
        return None  # Return None in case of any errors


async def fetch_setups_user(chat_id):
    supabase = connect_to_database()
    try:
        setup_number = (
            supabase.table("Setups")
            .select("*", count="exact")
            .eq("chat_id", chat_id)
            .execute()
        )

        if setup_number:
            return setup_number
            return None  # Return None if no data found for the chat_id
    except Exception as e:
        logger.info("An error occurred while fetching user's setups:", e)
        return None  # Return None in case of any errors


async def fetch_setup_wallet(wallet_address, chat_id):
    supabase = connect_to_database()
    try:
        setup_number = (
            supabase.table("Setups")
            .select("*", count="exact")
            .eq("wallet_address", wallet_address)
            .eq("chat_id", chat_id)
            .execute()
        )

        if setup_number:
            return setup_number
            return None  # Return None if no data found for the chat_id
    except Exception as e:
        logger.info("An error occurred while fetching user's wallet setups:", e)
        return None  # Return None in case of any errors


async def remove_setup_from_db(setup_id):
    supabase = connect_to_database()
    try:
        data = supabase.table("Setups").delete().eq("id", setup_id).execute()
    except Exception as e:
        logger.info("An error occurred while removing user's setup:", e)
        return None  # Return None in case of any errors


async def remove_all_from_db(chat_id):
    supabase = connect_to_database()
    try:
        data = supabase.table("Wallets").delete().eq("chat_id", chat_id).execute()
        data = supabase.table("Setups").delete().eq("chat_id", chat_id).execute()
    except Exception as e:
        logger.info("An error occurred while removing all user's data:", e)
        return None  # Return None in case of any errors


async def remove_wallet_and_alerts_from_db(chat_id, wallet_address):
    supabase = connect_to_database()
    try:
        # Delete the wallet associated with the specific chat_id and wallet_address
        wallet_delete_response = (
            supabase.table("Wallets")
            .delete()
            .eq("chat_id", chat_id)
            .eq("wallet_address", wallet_address)
            .execute()
        )
        # Delete the setups associated with the specific chat_id
        setups_delete_response = (
            supabase.table("Setups")
            .delete()
            .eq("chat_id", chat_id)
            .eq("wallet_address", wallet_address)
            .execute()
        )
    except Exception as e:
        logger.info("An error occurred while removing user's wallet and setups:", e)
        return None  # Return None in case of any errors


def fetch_token_symbol_for_contract(blockchain, contract_address):
    supabase = connect_to_database()
    try:
        data = (
            supabase.table("Contracts")
            .select("token_symbol")
            .ilike("blockchain", blockchain)
            .ilike("contract_address", contract_address)
            .execute()
        )
        return data.data[0]["token_symbol"]
    except Exception as e:
        logger.info(
            f"An error occurred while fetching token symbol for {contract_address} on {blockchain} :",
            e,
        )
        return None  # Return None in case of any errors


def fetch_decimal_for_contract(blockchain, contract_address):
    supabase = connect_to_database()
    try:
        data = (
            supabase.table("Contracts")
            .select("decimal")
            .ilike("blockchain", blockchain)
            .ilike("contract_address", contract_address)
            .execute()
        )
        return data.data[0]["decimal"]
    except Exception as e:
        logger.info(
            f"An error occurred while fetching decimal for {contract_address} on {blockchain} :",
            e,
        )
        return None  # Return None in case of any errors


def fetch_stake_for_wallet(wallet_address):
    supabase = connect_to_database()
    try:
        stake_data = (
            supabase.table("Setups")
            .select("stake_data")
            .ilike("wallet_address", wallet_address)
            .eq("token_symbol", "Stake Watch")
            .execute()
        )
        return stake_data.data[0]["stake_data"]
    except Exception as e:
        logger.info(
            f"An error occurred while fetching user's stake :",
            e,
        )
        return None  # Return None in case of any errors


def fetch_user_data(chat_id):
    supabase = connect_to_database()
    try:
        data = supabase.table("Users").select("*").eq("chat_id", chat_id).execute()
        return data.data
    except Exception as e:
        logger.info(
            f"An error occurred while fetching user's data :",
            e,
        )
        return None  # Return None in case of any errors


# def main():
#     stake_data = fetch_stake_for_wallet("0xcb2a9c1336c6cb83bf5453791138ed350c343bc5")

#     match_table = {
#         "eenp": "This is an Edge Node.",
#         "gcp": "This is a Guardian Node.",
#         "vcp": "This is a Validator Node.",
#     }

#     match_table_token = {
#         "eenp": "TFUEL",
#         "gcp": "THETA",
#         "vcp": "THETA.",
#     }

#     for record in stake_data["sourceRecords"]:
#         record_type = record["type"]
#         amount = int(record["amount"]) * (10**-18)
#         staked_value = record["withdrawn"]
#         # Format the amount with spaces every three digits
#         formatted_amount = "{:,.2f}".format(amount).replace(
#             ",", " "
#         )  # Replace commas with spaces
#         if record_type in match_table:
#             message = match_table[record_type]
#             token = match_table_token[record_type]
#             print(f"{message} with {formatted_amount} {token} staked.")
#             print(staked_value)


# def main():
#     data = fetch_user_data(1355080202)
#     print(data[0]["subscription"])


# if __name__ == "__main__":
#     main()
