import logging
import os
import re
import socket
import sqlite3
from collections import OrderedDict

from dotenv import load_dotenv
from httpcore import ConnectError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from database import (
    create_database,
    fetch_user_setups,
    insert_watch_data_to_db,
    remove_setup_from_database,
)

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="logs.log",
    encoding="utf-8",
    filemode="w",
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Import the token and connect to the bot
token = os.getenv("TELEGRAM_BOT_TOKEN")

watched_setups = []  # List to store the watched setups

# Expressions :
BTC_WALLET_ADDRESS_PATTERN = r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$"
THETA_WALLET_ADDRESS_PATTERN = r"^0x[a-fA-F0-9]{40}$"
BSC_WALLET_ADDRESS_PATTERN = r"^0x[a-fA-F0-9]{40}$"

BTC_CONTRACT_ADDRESS_PATTERN = None
THETA_CONTRACT_ADDRESS_PATTERN = r"^0x[a-fA-F0-9]{40}$"
BSC_CONTRACT_ADDRESS_PATTERN = r"^0x[a-fA-F0-9]{40}$"

CONTRACT_ADDRESS_PATTERN = r"^(0x)?[0-9a-fA-F]{40}$"

TOKEN_SYMBOL_PATTERN = r"^[A-Za-z0-9]+$"

# Predefined tokens and contract addresses
PREDEFINED_TOKENS = {
    "bitcoin": [{"symbol": "BTC", "contract_address": None}],
    "theta": [
        {"symbol": "THETA", "contract_address": None},
        {"symbol": "TFUEL", "contract_address": None},
        {
            "symbol": "TDROP",
            "contract_address": "0x1336739b05c7ab8a526d40dcc0d04a826b5f8b03",
        },
        {"symbol": "Stake Watch", "contract_address": None},
    ],
    "bsc": [{"symbol": "BNB", "contract_address": None}],
}


# Prompt a start message to the user
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # * Prints the username and chat_ID
    username = update.message.from_user.username
    chat_id = update.message.chat_id

    # Print the Telegram username and chat ID
    print(f"Telegram Username: {username}, Chat ID: {chat_id}")

    text = """Welcome to Crypto Wallet Monitor made by @TechSherpa.

This bot is here to help you keep an eye on your wallets and get alerted if new tokens arrive in your wallet!

You will be able to choose different wallets from different blockchains with a possibility to choose when to trigger an update.

Available commands are:
- 🌟 /addwatch - Add a brand new wallet to be closely monitored.
- ❌ /removewatch - Remove a setup from your monitored setups.
- 📋 /list - Get a comprehensive rundown of all your currently monitored wallets.
- ❓ /info - Get information about how the bot works and about your privacy.
"""

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


# Get some help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = """The bot is listening to your queries and stores your data in a database.

An important thing for me is to keep users anonymous so the only thing that is kept is your Chat_ID with the bot.
In that, he will know who to send messages to and not mix up the data from everyone.

Other than that, the bot doesn't log:
    - Your IP
    - Your username
    - Any other information that would identify you as a user.
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


create_database()


# Create a new setup to be watched
async def new_watch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""

    chat_id = update.effective_chat.id
    user_setups = fetch_user_setups(chat_id)

    if len(user_setups) >= 3:
        await update.message.reply_text(
            "You reached your limit. Delete a setup to add a new one."
        )
        return

    keyboard = [
        [
            InlineKeyboardButton("Bitcoin", callback_data="Bitcoin"),
            InlineKeyboardButton("Theta", callback_data="Theta"),
        ],
        [
            InlineKeyboardButton("BSC", callback_data="BSC"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Please choose a blockchain:", reply_markup=reply_markup
    )

    # Set the user's state to indicate that they are waiting for the blockchain selection
    context.user_data["state"] = "waiting_for_blockchain"


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    selected_blockchain = query.data

    state = context.user_data.get("state")

    if state == "waiting_for_blockchain":
        context.user_data["watch_data"] = {
            "chat_id": update.effective_chat.id,
            "blockchain": selected_blockchain,
            "balance": 0,
        }  # Add the chat_id as the first key
        await query.answer()
        await query.message.reply_text(f"You selected {selected_blockchain}.")

        if selected_blockchain.lower() == "bitcoin":
            context.user_data["watch_data"]["token_symbol"] = "BTC"
            await query.message.reply_text("Please enter your BTC wallet address:")
            context.user_data["state"] = "waiting_for_wallet_address"
        else:
            await query.message.reply_text("Please enter your wallet address:")
            context.user_data["state"] = "waiting_for_wallet_address"

    elif state == "waiting_for_token_details":
        if selected_blockchain.lower() == "other":
            await query.message.reply_text("Please enter the token address:")
            context.user_data["state"] = "waiting_for_token_details"

        elif selected_blockchain.lower() == "stake watch":
            watch_data = context.user_data.get("watch_data", {})
            watch_data["token_symbol"] = selected_blockchain
            context.user_data["watch_data"] = watch_data
            await query.answer()
            await query.message.reply_text(
                "Your stake is being watched. Setup complete."
            )
            context.user_data["state"] = None

        else:
            predefined_tokens = PREDEFINED_TOKENS.get(
                context.user_data["watch_data"]["blockchain"].lower(), []
            )
            selected_token = next(
                (
                    token
                    for token in predefined_tokens
                    if token["symbol"] == selected_blockchain
                ),
                None,
            )
            if selected_token:
                watch_data = context.user_data.get("watch_data", {})
                watch_data["token_symbol"] = selected_token["symbol"]
                watch_data["contract_address"] = selected_token["contract_address"]
                context.user_data["watch_data"] = watch_data
                await query.answer()
                await query.message.reply_text(f"You selected {selected_blockchain}.")
                await query.message.reply_text(
                    "Please enter the trigger point as an integer <i>(choose 0 if you want to see every update)</i>:",
                    parse_mode="HTML",
                )
                context.user_data["state"] = "waiting_for_trigger_point"
            else:
                await query.answer()

    elif state == "waiting_for_wallet_name":
        if selected_blockchain.lower() == "name_wallet_yes":
            await query.answer()
            await query.message.reply_text("Please enter the name for your wallet:")
            context.user_data["state"] = "waiting_for_wallet_name_input"
        elif selected_blockchain.lower() == "name_wallet_no":
            await query.answer()
            predefined_tokens = PREDEFINED_TOKENS.get(
                context.user_data["watch_data"]["blockchain"].lower(), []
            )
            keyboard = [
                [InlineKeyboardButton(token["symbol"], callback_data=token["symbol"])]
                for token in predefined_tokens
            ]
            keyboard.append([InlineKeyboardButton("Other", callback_data="Other")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                "Please make a choice:", reply_markup=reply_markup
            )
            context.user_data["watch_data"]["wallet_name"] = None
            context.user_data["state"] = "waiting_for_token_details"

    elif state == "waiting_for_setup_number":
        query = update.callback_query
        chat_id = query.message.chat_id
        selected_setup_number = int(query.data)

        user_setups = fetch_user_setups(chat_id)

        removed_setup = user_setups[selected_setup_number - 1]

        # Remove the setup from the database
        remove_setup_from_database(removed_setup)

        # Print the removed_setup object
        print("removed_setup:", removed_setup)

        await query.answer("Setup removed successfully.")
        await query.message.reply_text(
            f"Setup Number {selected_setup_number} removed successfully."
        )
        logging.info(
            "Chat ID %s removed successfully setup number %s.",
            chat_id,
            selected_setup_number,
        )

        # Clear the user's state
        del context.user_data["state"]

    else:
        await query.answer()


# Parse the user input and add it to a dictionary -> To be put into a DB
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text.strip()
    state = context.user_data.get("state")

    if state == "waiting_for_blockchain":
        context.user_data["watch_data"] = {
            "chat_id": update.effective_chat.id,
            "blockchain": message.capitalize(),
            "balance": 0,
        }
        # context.user_data["watch_data"]["chat_id"] = update.effective_chat.id
        # context.user_data["watch_data"]["blockchain"] = message.capitalize()
        # context.user_data["watch_data"]["balance"] = 0
        await update.message.reply_text(f"You selected {message}.")

        if message.lower() == "bitcoin":
            context.user_data["watch_data"]["token_symbol"] = "BTC"
            await update.message.reply_text("Please enter your BTC wallet address:")
            context.user_data["state"] = "waiting_for_wallet_address"
        elif message.lower() == "theta":
            await update.message.reply_text("Please enter your Theta wallet address:")
            context.user_data["state"] = "waiting_for_wallet_address"
        elif message.lower() == "bsc":
            await update.message.reply_text("Please enter your BSC wallet address:")
            context.user_data["state"] = "waiting_for_wallet_address"
        else:
            await update.message.reply_text(
                "Invalid blockchain. Please choose a valid blockchain."
            )
            return

    elif state == "waiting_for_wallet_address":
        if context.user_data["watch_data"]["blockchain"].lower() == "bitcoin":
            pattern = BTC_WALLET_ADDRESS_PATTERN
        elif context.user_data["watch_data"]["blockchain"].lower() == "theta":
            pattern = THETA_WALLET_ADDRESS_PATTERN
        else:
            pattern = BSC_WALLET_ADDRESS_PATTERN

        if re.match(pattern, message):
            watch_data = context.user_data.get("watch_data", {})
            watch_data["wallet_address"] = message
            context.user_data["watch_data"] = watch_data

            # Prompt the user to name the wallet
            keyboard = [
                [InlineKeyboardButton("Yes", callback_data="name_wallet_yes")],
                [InlineKeyboardButton("No", callback_data="name_wallet_no")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "Do you want to name that wallet?", reply_markup=reply_markup
            )

            context.user_data["state"] = "waiting_for_wallet_name"
        else:
            await update.message.reply_text(
                "Invalid wallet address. Please enter a valid address."
            )
            return

    elif state == "waiting_for_wallet_address":
        if context.user_data["watch_data"]["blockchain"].lower() == "bitcoin":
            pattern = BTC_WALLET_ADDRESS_PATTERN
        elif context.user_data["watch_data"]["blockchain"].lower() == "theta":
            pattern = THETA_WALLET_ADDRESS_PATTERN
        else:
            pattern = BSC_WALLET_ADDRESS_PATTERN

        if re.match(pattern, message):
            watch_data = context.user_data.get("watch_data", {})
            watch_data["wallet_address"] = message
            context.user_data["watch_data"] = watch_data
            await update.message.reply_text(f"Your wallet address: {message}.")

            if (
                context.user_data["watch_data"]["blockchain"].lower()
                in PREDEFINED_TOKENS
            ):
                predefined_tokens = PREDEFINED_TOKENS[
                    context.user_data["watch_data"]["blockchain"].lower()
                ]
                keyboard = [
                    [
                        InlineKeyboardButton(
                            token["symbol"], callback_data=token["symbol"]
                        )
                    ]
                    for token in predefined_tokens
                ]
                keyboard.append([InlineKeyboardButton("Other", callback_data="Other")])
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(
                    "Please choose a token:", reply_markup=reply_markup
                )
                context.user_data["state"] = "waiting_for_token_details"
            else:
                await update.message.reply_text("Please enter the token address:")
                context.user_data["state"] = "waiting_for_token_details"
        else:
            await update.message.reply_text(
                "Invalid wallet address. Please enter a valid address."
            )
            return

    elif state == "waiting_for_token_details":
        predefined_tokens = PREDEFINED_TOKENS.get(
            context.user_data["watch_data"]["blockchain"].lower(), []
        )
        selected_token = next(
            (
                token
                for token in predefined_tokens
                if token["symbol"].lower() == message.lower()
            ),
            None,
        )
        if selected_token:
            watch_data = context.user_data.get("watch_data", {})
            watch_data["token_symbol"] = selected_token["symbol"]
            watch_data["contract_address"] = selected_token["contract_address"]
            context.user_data["watch_data"] = watch_data
            await update.message.reply_text(f"You selected {message}.")
            await update.message.reply_text(
                "Please enter the trigger point as an integer "
                "<i>(choose 0 if you want to see every update)</i>:",
                parse_mode="HTML",
            )
            context.user_data["state"] = "waiting_for_trigger_point"
        elif message.lower() == "other":
            await update.message.reply_text("Please enter the token address:")
            context.user_data["state"] = "waiting_for_token_address"
        else:
            await update.message.reply_text(
                f"Invalid token. Please choose a token from the predefined options."
            )
            return

    elif state == "waiting_for_token_address":
        watch_data = context.user_data.get("watch_data", {})
        watch_data["contract_address"] = message
        context.user_data["watch_data"] = watch_data
        await update.message.reply_text(f"Your token address: {message}.")
        await update.message.reply_text("Please enter the token symbol:")
        context.user_data["state"] = "waiting_for_token_symbol"

    elif state == "waiting_for_token_symbol":
        watch_data = context.user_data.get("watch_data", {})
        watch_data["token_symbol"] = message
        context.user_data["watch_data"] = watch_data
        await update.message.reply_text(f"Your token symbol: {message}.")
        await update.message.reply_text(
            "Please enter the trigger point as an integer "
            "<i>(choose 0 if you want to see every update)</i>:",
            parse_mode="HTML",
        )
        context.user_data["state"] = "waiting_for_trigger_point"

    elif state == "waiting_for_trigger_point":
        try:
            # Replace comma with period for European number format
            message = message.replace(",", ".")

            trigger_point = float(message)
            watch_data = context.user_data.get("watch_data", {})
            watch_data["trigger_point"] = trigger_point
            context.user_data["watch_data"] = watch_data

            chat_id = update.effective_chat.id
            existing_setup = fetch_user_setups(chat_id)
            # Check if the setup already exists
            existing_setup = next(
                (
                    setup
                    for setup in watched_setups
                    if setup["watch_data"] == watch_data
                ),
                None,
            )

            if existing_setup:
                await update.message.reply_text("This setup already exists.")
                return

            await update.message.reply_text(f"Your trigger point: {trigger_point}.")
            await update.message.reply_text("Watch setup completed.")

            context.user_data["watch_data"] = watch_data
            insert_watch_data_to_db(context.user_data["watch_data"])

            # Add the watch_data to the watched_setups list
            chat_id = update.effective_chat.id
            watched_setups.append(
                {"watch_data": context.user_data["watch_data"], "chat_id": chat_id}
            )

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
            context.user_data["watch_data"] = ordered_watch_data

            # Reset the user's state
            context.user_data["state"] = None

            # Print the watch_data dictionary
            print("User data:", context.user_data["watch_data"])
            logger.info("Setup completed: %s", context.user_data["watch_data"])

        except ValueError:
            await update.message.reply_text(
                "Invalid trigger point. Please enter an integer."
            )

            # Stay in the same state and prompt for the trigger point again
            context.user_data["state"] = "waiting_for_trigger_point"

    elif state == "waiting_for_setup_number":
        # Ignore any text messages received while waiting for setup number selection
        await update.message.reply_text("Please use the buttons.")
        return

    elif state == "waiting_for_wallet_name_input":
        watch_data = context.user_data.get("watch_data", {})
        watch_data["wallet_name"] = message
        context.user_data["watch_data"] = watch_data
        await update.message.reply_text(f"You named the wallet: {message}.")
        predefined_tokens = PREDEFINED_TOKENS.get(
            context.user_data["watch_data"]["blockchain"].lower(), []
        )
        keyboard = [
            [InlineKeyboardButton(token["symbol"], callback_data=token["symbol"])]
            for token in predefined_tokens
        ]
        keyboard.append([InlineKeyboardButton("Other", callback_data="Other")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Please choose a token:", reply_markup=reply_markup
        )
        context.user_data["state"] = "waiting_for_token_details"

    elif state == "waiting_for_wallet_name":
        # Ignore any text messages received while waiting for setup number selection
        await update.message.reply_text("Please use the buttons.")
        return

    else:
        await update.message.reply_text("Invalid input.")

        # Reset the user's state if an invalid input is given
        context.user_data["state"] = None


async def removewatch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id

    user_setups = fetch_user_setups(chat_id)
    print(user_setups)

    if user_setups:
        text = "List of watched setups:\n"
        for i, setup in enumerate(user_setups):
            text += f"\n<b><u>Setup {str(i+1)}:</u></b>"
            if setup["wallet_name"] in setup:
                text += f"\nWallet Name: {setup['wallet_name']}"
            text += f"\nBlockchain: {setup['blockchain'].capitalize()}"
            text += f"\nWallet Address: {setup['wallet_address']}"
            if "contract_address" in setup:
                text += f"\nContract Address: {setup['contract_address']}"
            if "token_symbol" in setup:
                text += f"\nToken Symbol: {setup['token_symbol']}"
            if "trigger_point" in setup:
                text += f"\nTrigger Point: {setup['trigger_point']}"
            # if "balance" in setup:
            #     text += f"\nBalance: {setup['balance']} {setup['token_symbol']} "
            text += "\n"

        await update.message.reply_text(text, parse_mode="HTML")

        # Prepare a list of setup numbers for user selection
        setup_numbers = [str(i + 1) for i in range(len(user_setups))]
        keyboard = [
            [InlineKeyboardButton(number, callback_data=number)]
            for number in setup_numbers
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "Which setup would you like to remove?", reply_markup=reply_markup
        )

        # Set the user's state to indicate that they are waiting for the setup number
        context.user_data["state"] = "waiting_for_setup_number"
    else:
        await update.message.reply_text("No watched setups available.")


async def list_watched_setups(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id

    user_setups = fetch_user_setups(chat_id)

    if user_setups:
        text = "List of watched setups:\n"
        for i, setup in enumerate(user_setups):
            text += f"\n<b><u>Setup {i+1}:</u></b>"
            if setup["wallet_name"]:
                text += f"\nWallet Name: {setup['wallet_name']}"
            text += f"\nBlockchain: {setup['blockchain'].capitalize()}"
            text += f"\nWallet Address: {setup['wallet_address']}"
            if setup["contract_address"]:
                text += f"\nContract Address: {setup['contract_address']}"
            if setup["token_symbol"]:
                text += f"\nToken Symbol: {setup['token_symbol']}"
            if setup["trigger_point"]:
                text += f"\nTrigger Point: {setup['trigger_point']}"
            # if "balance" in setup:
            #     text += f"\nBalance: {setup['balance']} {setup['token_symbol']} "
            text += "\n"

            logger.info("Chat ID %s is running the list command.", chat_id)

        await update.message.reply_text(text, parse_mode="HTML")
    else:
        logger.info("Chat ID %s is running the list command with no setups.", chat_id)
        await update.message.reply_text("No watched setups available.")


if __name__ == "__main__":
    print("Starting bot ...")
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addwatch", new_watch))
    application.add_handler(CommandHandler("removewatch", removewatch))
    application.add_handler(CommandHandler("list", list_watched_setups))
    application.add_handler(CommandHandler("info", help))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.Text(), handle_message))

    try:
        print("Start polling ...")
        application.run_polling()
    except ConnectError as e:
        logging.error(f"Error while getting Updates: {e}")
    except socket.gaierror as e:
        logging.error(f"Error resolving hostname: {e}")
