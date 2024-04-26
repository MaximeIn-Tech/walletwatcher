import logging
import os
import re
import socket
from enum import Enum

from dotenv import load_dotenv
from httpcore import ConnectError
from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    Updater,
    filters,
)

from menus import *
from messages import *

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


############################ Expressions #######################################

BTC_WALLET_ADDRESS_PATTERN = r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$"
THETA_WALLET_ADDRESS_PATTERN = r"^0x[a-fA-F0-9]{40}$"
BSC_WALLET_ADDRESS_PATTERN = r"^0x[a-fA-F0-9]{40}$"

BTC_CONTRACT_ADDRESS_PATTERN = None
THETA_CONTRACT_ADDRESS_PATTERN = r"^0x[a-fA-F0-9]{40}$"
BSC_CONTRACT_ADDRESS_PATTERN = r"^0x[a-fA-F0-9]{40}$"

# Combine all wallet address patterns into a single pattern
WALLET_ADDRESS_PATTERN = re.compile(
    f"({'|'.join([BTC_WALLET_ADDRESS_PATTERN, THETA_WALLET_ADDRESS_PATTERN, BSC_WALLET_ADDRESS_PATTERN])})"
)

CONTRACT_ADDRESS_PATTERN = r"^(0x)?[0-9a-fA-F]{40}$"

# Combine all contract address patterns into a single pattern
CONTRACT_ADDRESS_PATTERN = re.compile(
    f"({'|'.join([THETA_CONTRACT_ADDRESS_PATTERN, BSC_CONTRACT_ADDRESS_PATTERN])})"
)


TOKEN_SYMBOL_PATTERN = r"^[A-Za-z0-9]+$"

####### Predefined tokens and contract addresses ##########


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
    "eth": [{"symbol": "ETH", "contract_address": None}],
    "bsc": [{"symbol": "BNB", "contract_address": None}],
}


############################ Bot Menus #########################################


async def start(update, context):
    username = update.message.from_user.first_name
    user_language_from_telegram_options = update.effective_user.language_code
    context.user_data["language"] = user_language_from_telegram_options
    context.user_data["name"] = username
    await update.message.reply_text(
        await main_menu_message(username), reply_markup=await main_menu_keyboard()
    )


async def main_menu(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=await main_menu_message(query.from_user.first_name),
        reply_markup=await main_menu_keyboard(),
    )


async def help(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=await help_message(),
        reply_markup=await back_to_to_main_keyboard(),
    )


############################ Add Track #########################################


# STEP 1 : Handle blockchain selection
async def track_sub_menu_1(update, context):
    query = update.callback_query
    context.user_data["chat_id"] = query.message.chat_id
    await query.answer()
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="Please select a blockchain:",
        reply_markup=await blockchain_keyboard(),
    )


async def blockchain_selection(update, context):
    query = update.callback_query
    selected_blockchain = str(
        query.data
    ).capitalize()  # This will contain the selected blockchain
    context.user_data["blockchain"] = selected_blockchain
    # Remember the selected blockchain or perform any other action
    await query.answer(text=f"You selected {selected_blockchain}")
    await prompt_wallet_address_input(update, context, selected_blockchain)


async def prompt_wallet_address_input(update, context, selected_blockchain):
    selected_blockchain = selected_blockchain.upper()
    text = f"Please enter any {selected_blockchain} wallet address:"
    await context.bot.send_message(
        chat_id=update.callback_query.message.chat_id, text=text
    )


# STEP 2 : Handle wallet address input
async def handle_messages(update, context):
    if context.user_data.get("is_entering_wallet_name", False):
        await handle_wallet_name(update, context)
    elif context.user_data.get("is_entering_trigger_point", False):
        await handle_trigger_point(update, context)
    elif context.user_data.get("is_entering_contract_address", False):
        await handle_contract_address(update, context)
    else:
        await handle_wallet_address(update, context)


# STEP 3 : Name the wallet.
async def naming_wallet_selection(update, context):
    query = update.callback_query
    selected_option = query.data
    await query.answer()

    if selected_option == "yes":
        context.user_data["is_entering_wallet_name"] = True
        await context.bot.send_message(
            chat_id=context.user_data["chat_id"],
            text="Please enter the name of the wallet:",
        )

    elif selected_option == "no":
        context.user_data["wallet_name"] = "None"
        await select_token_symbol(update, context)

    elif selected_option == "main":
        await main_menu(update, context)


async def handle_wallet_address(update, context):
    wallet_address = update.message.text

    # Check if the wallet address matches the pattern
    if WALLET_ADDRESS_PATTERN.match(wallet_address):
        # Store the wallet address in the user data for later use if needed
        context.user_data["wallet_address"] = wallet_address
        await context.bot.send_message(
            chat_id=context.user_data["chat_id"],
            text=f"Your wallet address is {wallet_address}.\nWould you like to name that address?",
            reply_markup=await naming_wallet_keyboard(),
        )
    else:
        await context.bot.send_message(
            chat_id=context.user_data["chat_id"],
            text="Please enter a valid wallet address.",
        )


async def handle_wallet_name(update, context):
    wallet_name = update.message.text
    context.user_data["wallet_name"] = wallet_name
    await select_token_symbol(update, context)  # Corrected function call
    context.user_data.pop(
        "is_entering_wallet_name", None
    )  # Remove the key if it exists


# STEP 4:
async def select_token_symbol(update, context):
    selected_blockchain = context.user_data.get("blockchain", "").lower()
    predefined_tokens = PREDEFINED_TOKENS.get(selected_blockchain, [])
    keyboard = [
        [InlineKeyboardButton(token["symbol"], callback_data=token["symbol"])]
        for token in predefined_tokens
    ]
    keyboard.append([InlineKeyboardButton("Other", callback_data="Other")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=context.user_data["chat_id"],
        text="Please select a token symbol",
        reply_markup=reply_markup,
    )


async def handle_selected_token(update, context):
    query = update.callback_query
    selected_token = query.data.split("_")[0]  # Extract selected token symbol
    selected_blockchain = context.user_data.get("blockchain", "").lower()
    predefined_tokens = PREDEFINED_TOKENS.get(selected_blockchain, [])

    if selected_token.lower() == "other":
        await context.bot.send_message(
            chat_id=update.callback_query.message.chat_id,
            text="Please enter the contract address",
        )
        # Set a flag in user_data to indicate that we are waiting for the contract address
        context.user_data["is_entering_contract_address"] = True
    else:
        selected_token_info = next(
            (token for token in predefined_tokens if token["symbol"] == selected_token),
            None,
        )
        if selected_token_info:
            selected_symbol = selected_token_info["symbol"]
            contract_address = selected_token_info["contract_address"]
            await query.answer(
                f"You selected {selected_symbol} with contract address {contract_address}"
            )
            # Now you can use selected_symbol and contract_address as needed
            # For example, store them in user_data
            context.user_data["selected_symbol"] = selected_symbol
            context.user_data["contract_address"] = contract_address

            # Check if the selected blockchain is Theta and the selected token is "Stake Watch"
            if (
                selected_blockchain == "theta"
                and selected_symbol.lower() == "stake watch"
            ):
                await context.bot.send_message(
                    chat_id=update.callback_query.message.chat_id,
                    text=await stake_message(),
                    reply_markup=await back_to_to_main_keyboard(),
                )
            else:
                # Proceed with trigger point prompt
                await prompt_trigger_point(update, context)
        else:
            await query.answer("Invalid selection")


async def handle_contract_address(update, context):
    contract_address = update.message.text

    # Check if the contract address matches the pattern
    if re.match(CONTRACT_ADDRESS_PATTERN, contract_address):
        # Store the contract address in the user data
        context.user_data["contract_address"] = contract_address
        await context.bot.send_message(
            chat_id=context.user_data["chat_id"],
            text=f"Contract address {contract_address} saved.",
        )
        await prompt_trigger_point(update, context)
    else:
        # Send a message informing the user that the entered contract address is invalid
        await context.bot.send_message(
            chat_id=context.user_data["chat_id"],
            text="Please enter a valid contract address.",
        )


# STEP 6: TRIGGER POINT
async def prompt_trigger_point(update, context):
    await context.bot.send_message(
        chat_id=context.user_data["chat_id"],
        text="Please enter the trigger point as an integer <i>(choose 0 if you want to see every update)</i>:",
        parse_mode="HTML",
    )
    context.user_data["is_entering_trigger_point"] = True


async def handle_trigger_point(update, context):
    trigger_point = update.message.text

    try:
        # Try converting the input to a float
        trigger_point_float = float(trigger_point)
        # Store the trigger point as a float
        context.user_data["trigger_point"] = trigger_point_float
        await context.bot.send_message(
            chat_id=context.user_data["chat_id"],
            text=f"Trigger point {trigger_point_float} saved.",
        )
    except ValueError:
        try:
            # Try converting the input to an integer
            trigger_point_int = int(trigger_point)
            # Store the trigger point as an integer
            context.user_data["trigger_point"] = trigger_point_int
            await context.bot.send_message(
                chat_id=context.user_data["chat_id"],
                text=f"Trigger point {trigger_point_int} saved.",
            )
        except ValueError:
            # Send a message informing the user that the entered trigger point is invalid
            await context.bot.send_message(
                chat_id=context.user_data["chat_id"],
                text="Please enter a valid trigger point as an integer or float.",
            )
            return  # Stop further execution if the trigger point is invalid

    # Remove the is_entering_trigger_point flag after successfully storing the trigger point
    context.user_data.pop("is_entering_trigger_point", None)

    # Prompt the user with the saved setup
    await prompt_tracked_wallet(context)
    print(context.user_data)


# COMPLETED:


async def prompt_tracked_wallet(context):
    blockchain = context.user_data.get("blockchain")
    wallet_address = context.user_data.get("wallet_address")
    wallet_name = context.user_data.get("wallet_name")
    symbol = context.user_data.get("selected_symbol")
    contract_address = context.user_data.get("contract_address")
    trigger_point = context.user_data.get("trigger_point")

    message = f"Tracked wallet setup:\n\n"
    message += f"Wallet Name: {wallet_name}\n"
    message += f"Blockchain: {blockchain}\n"
    message += f"Wallet Address: {wallet_address}\n"
    message += f"Token Symbol: {symbol}\n"
    if contract_address is not None:
        message += f"Contract Address: {contract_address}\n"
    message += f"Trigger Point: {trigger_point}"

    await context.bot.send_message(
        chat_id=context.user_data["chat_id"],
        text=message,
        reply_markup=await back_to_to_main_keyboard(),
    )


############################ Settings Menus ####################################


async def settings_menu(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=await settings_message(),
        reply_markup=await settings_menu_keyboard(),
    )


async def language_selection_menu(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=await language_selection_message(),
        reply_markup=await language_keyboard(),
    )


if __name__ == "__main__":
    print("Starting bot ...")
    application = Application.builder().token(token).build()

    ############################ BUTTON INTERACTION HANDLERS ###################
    ############################ Main Menu Handlers ############################

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(main_menu, pattern="main"))
    application.add_handler(CallbackQueryHandler(help, pattern="help_menu"))

    ############################ Add Track Handlers ############################
    application.add_handler(
        CallbackQueryHandler(track_sub_menu_1, pattern="track_menu")
    )
    application.add_handler(
        CallbackQueryHandler(blockchain_selection, pattern=r"^(theta|bsc|eth)$")
    )

    ############################ Setting Handlers ##############################
    application.add_handler(
        CallbackQueryHandler(settings_menu, pattern="settings_menu")
    )
    application.add_handler(
        CallbackQueryHandler(language_selection_menu, pattern="language_menu")
    )

    ############################ Naming Wallet Handlers #########################################
    application.add_handler(
        CallbackQueryHandler(naming_wallet_selection, pattern=r"^(yes|no)$")
    )

    application.add_handler(CallbackQueryHandler(handle_selected_token))

    ############################ MESSAGE HANDLERS ############################
    ############################ Add Track Handlers ############################
    application.add_handler(MessageHandler(filters.Text(), handle_messages))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

    print("Start polling ...")

    application.run_polling(allowed_updates=Update.ALL_TYPES)
