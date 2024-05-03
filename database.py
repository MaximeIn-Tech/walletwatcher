"""
NOTE : This file is here to handle all the database interaction.
"""

import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()


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
        print("An error occurred:", e)
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
        print("An error occurred:", e)
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
        print("An error occurred:", e)
        return None  # Return None in case of any errors


async def fetch_contract_user(chat_id):
    supabase = connect_to_database()
    try:
        contract_number = (
            supabase.table("Contracts")
            .select("*", count="exact")
            .eq("chat_id", chat_id)
            .execute()
        )

        if contract_number:
            return contract_number
            return None  # Return None if no data found for the chat_id
    except Exception as e:
        print("An error occurred:", e)
        return None  # Return None in case of any errors


async def fetch_contract_wallet(wallet_address):
    supabase = connect_to_database()
    try:
        contract_number = (
            supabase.table("Contracts")
            .select("*", count="exact")
            .eq("wallet_address", wallet_address)
            .execute()
        )

        if contract_number:
            return contract_number
            return None  # Return None if no data found for the chat_id
    except Exception as e:
        print("An error occurred:", e)
        return None  # Return None in case of any errors
