"""
NOTE : This file is here to handle all the database interaction.
TODO: I need to create a way to connect to the DB, add a user, fetch a user info, add a wallet, fetch the data from the wallet tables, add a contract and fetch the contract table.
TODO : Add the keys of the database to the .env file
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
