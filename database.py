import sqlite3


def create_database():
    # Establish a connection to the SQLite database
    conn = sqlite3.connect("watched_setups.db")
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS watched_setups (
            chat_id INTEGER,
            blockchain TEXT,
            wallet_address TEXT,
            wallet_name TEXT,
            token_symbol TEXT,
            contract_address TEXT,
            trigger_point REAL,
            balance REAL
        )
    """
    )

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Function for the database
def insert_watch_data_to_db(watch_data):
    # Establish a connection to the SQLite database
    conn = sqlite3.connect("watched_setups.db")
    cursor = conn.cursor()

    # Reorder the watch_data dictionary
    ordered_watch_data = OrderedDict(
        (key, watch_data[key])
        for key in [
            "chat_id",
            "blockchain",
            "wallet_address",
            "wallet_name",
            "token_symbol",
            "contract_address",
            "trigger_point",
            "balance",
        ]
    )

    # Set the initial balance to 0 if not already set
    if "balance" not in ordered_watch_data:
        ordered_watch_data["balance"] = 0.0

    # Insert the watch_data into the database
    query = """
        INSERT INTO watched_setups (chat_id, blockchain, wallet_address, wallet_name, token_symbol, contract_address, trigger_point, balance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    data = (
        ordered_watch_data["chat_id"],
        ordered_watch_data["blockchain"],
        ordered_watch_data["wallet_address"],
        ordered_watch_data["wallet_name"],
        ordered_watch_data["token_symbol"],
        ordered_watch_data["contract_address"],
        ordered_watch_data["trigger_point"],
        ordered_watch_data["balance"],
    )
    cursor.execute(query, data)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def fetch_user_setups(chat_id):
    # Establish a connection to the SQLite database
    conn = sqlite3.connect("watched_setups.db")
    cursor = conn.cursor()

    # Fetch the user setups from the database
    query = """
        SELECT chat_id, blockchain, wallet_address, wallet_name, token_symbol, contract_address, trigger_point, balance
        FROM watched_setups
        WHERE chat_id = ?
    """
    cursor.execute(query, (chat_id,))
    rows = cursor.fetchall()

    # Populate the user_setups list
    user_setups = []
    for row in rows:
        setup = {
            "chat_id": row[0],
            "blockchain": row[1],
            "wallet_address": row[2],
            "wallet_name": row[3],
            "token_symbol": row[4],
            "contract_address": row[5],
            "trigger_point": row[6],
            "balance": row[7],
        }
        user_setups.append(setup)

    conn.close()

    return user_setups


def remove_setup_from_database(setup_to_remove):
    print("Setup to be removed:", setup_to_remove)

    # Establish a connection to the SQLite database
    conn = sqlite3.connect("watched_setups.db")
    cursor = conn.cursor()

    # Remove the setup from the database based on chat_id and setup details
    query = """
        DELETE FROM watched_setups
        WHERE chat_id = ? AND blockchain = ? AND wallet_address = ? AND wallet_name = ? AND token_symbol = ?
        AND (contract_address = ? OR contract_address IS NULL) AND trigger_point = ? AND balance = ?;
    """
    data = (
        setup_to_remove["chat_id"],
        setup_to_remove["blockchain"],
        setup_to_remove["wallet_address"],
        setup_to_remove["wallet_name"],
        setup_to_remove["token_symbol"],
        setup_to_remove["contract_address"],
        setup_to_remove["trigger_point"],
        setup_to_remove["balance"],
    )
    cursor.execute(query, data)
    conn.commit()
    conn.close()
