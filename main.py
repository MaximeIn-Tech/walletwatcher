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

from database import *
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

supabase = connect_to_database()

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
    language = await get_language_for_chat_id(update.effective_chat.id)
    try:
        context.user_data["chat_id"] = update.effective_chat.id
        context.user_data["language"] = language
        context.user_data["name"] = update.message.from_user.first_name
        print(context.user_data["chat_id"])
        # Check if the user already exists in the Users table
        existing_user = (
            supabase.table("Users")
            .select("*")
            .eq("chat_id", context.user_data["chat_id"])
            .execute()
        )
        print(existing_user)

        if not existing_user.data:
            # User does not exist, insert new record
            data, count = (
                supabase.table("Users")
                .insert(
                    {
                        "chat_id": context.user_data["chat_id"],
                        "language": context.user_data["language"],
                    }
                )
                .execute()
            )
            print("User added")
        else:
            print("User already exists")

        # Reply to the user
        await update.message.reply_text(
            await main_menu_message(context.user_data["name"], language),
            reply_markup=await main_menu_keyboard(language),
        )
    except Exception as e:
        print("An error occurred:", e)


async def main_menu(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    print(language)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=await main_menu_message(query.from_user.first_name, language),
        reply_markup=await main_menu_keyboard(language),
    )


async def help(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=await help_message(language),
        reply_markup=await back_to_to_main_keyboard(language),
    )


############################ Add Track #########################################
"""
TODO: 
- Show a menu when the user clicks on "Track" that shows all the wallets that are in the database for that user. If there is none, don't ask for that menu. If there are wallets, also add a button to add a new wallet (and watch).
- The wallet is the only thing that will be able to be selected. I also need to add that to the remove section -> Wallet selection than a list of all contracts/setups for that wallet.
- Maybe add a delete all button too with a confirmation.
"""


# STEP 1 : Handle blockchain selection
async def track_sub_menu_1(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    context.user_data["chat_id"] = query.message.chat_id
    await query.answer()
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=await blockchain_choice_message(language),
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
    language = await get_language_for_chat_id(update.effective_chat.id)
    selected_blockchain = selected_blockchain.upper()
    text = await address_choice_message(language, selected_blockchain)
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
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    selected_option = query.data
    await query.answer()

    if selected_option == "yes":
        context.user_data["is_entering_wallet_name"] = True
        await context.bot.send_message(
            chat_id=context.user_data["chat_id"],
            text=await naming_wallet(language),
        )

    elif selected_option == "no":
        context.user_data["wallet_name"] = "None"
        await select_token_symbol(update, context)

    elif selected_option == "main":
        await main_menu(update, context)


async def handle_wallet_address(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    wallet_address = update.message.text

    # Check if the wallet address matches the pattern
    if WALLET_ADDRESS_PATTERN.match(wallet_address):
        # Store the wallet address in the user data for later use if needed
        context.user_data["wallet_address"] = wallet_address
        await context.bot.send_message(
            chat_id=context.user_data["chat_id"],
            text=await address_confirmation_message(language, wallet_address),
            reply_markup=await naming_wallet_keyboard(language),
        )
    else:
        await context.bot.send_message(
            chat_id=context.user_data["chat_id"],
            text=await wallet_address_error(language),
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
    language = await get_language_for_chat_id(update.effective_chat.id)
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
        text=await token_symbol_choice(language),
        reply_markup=reply_markup,
    )


async def handle_selected_token(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    selected_token = query.data.split("_")[0]  # Extract selected token symbol
    selected_blockchain = context.user_data.get("blockchain", "").lower()
    predefined_tokens = PREDEFINED_TOKENS.get(selected_blockchain, [])

    if selected_token.lower() == "other":
        await context.bot.send_message(
            chat_id=update.callback_query.message.chat_id,
            text=await contract_address_selection(language),
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
                    text=await stake_message(language),
                    reply_markup=await back_to_to_main_keyboard(language),
                )
            else:
                # Proceed with trigger point prompt
                await prompt_trigger_point(update, context)
        else:
            await query.answer("Invalid selection")


async def handle_contract_address(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    contract_address = update.message.text

    # Check if the contract address matches the pattern
    if re.match(CONTRACT_ADDRESS_PATTERN, contract_address):
        # Store the contract address in the user data
        context.user_data["contract_address"] = contract_address
        await context.bot.send_message(
            chat_id=context.user_data["chat_id"],
            text=await custom_contract_address(language, contract_address),
        )
        await prompt_trigger_point(update, context)
    else:
        # Send a message informing the user that the entered contract address is invalid
        await context.bot.send_message(
            chat_id=context.user_data["chat_id"],
            text=await contract_address_error(language),
        )


# STEP 6: TRIGGER POINT
async def prompt_trigger_point(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    await context.bot.send_message(
        chat_id=context.user_data["chat_id"],
        text=await trigger_point_selection(language),
        parse_mode="HTML",
    )
    context.user_data["is_entering_trigger_point"] = True


async def handle_trigger_point(update, context):
    trigger_point = update.message.text
    language = await get_language_for_chat_id(update.effective_chat.id)

    try:
        # Try converting the input to a float
        trigger_point_float = float(trigger_point)
        # Store the trigger point as a float
        context.user_data["trigger_point"] = trigger_point_float
        await context.bot.send_message(
            chat_id=context.user_data["chat_id"],
            text=await trigger_point_saved(language, trigger_point_float),
        )
    except ValueError:
        try:
            # Try converting the input to an integer
            trigger_point_int = int(trigger_point)
            # Store the trigger point as an integer
            context.user_data["trigger_point"] = trigger_point_int
            await context.bot.send_message(
                chat_id=context.user_data["chat_id"],
                text=await trigger_point_saved(language, trigger_point_int),
            )
        except ValueError:
            # Send a message informing the user that the entered trigger point is invalid
            await context.bot.send_message(
                chat_id=context.user_data["chat_id"],
                text=await trigger_point_error(language),
            )
            return  # Stop further execution if the trigger point is invalid

    # Remove the is_entering_trigger_point flag after successfully storing the trigger point
    context.user_data.pop("is_entering_trigger_point", None)

    # Prompt the user with the saved setup
    await prompt_tracked_wallet(context)
    print(context.user_data)


# COMPLETED:


async def prompt_tracked_wallet(context):
    language = context.user_data["language"]
    blockchain = context.user_data.get("blockchain")
    wallet_address = context.user_data.get("wallet_address")
    wallet_name = context.user_data.get("wallet_name")
    symbol = context.user_data.get("selected_symbol")
    contract_address = context.user_data.get("contract_address")
    trigger_point = context.user_data.get("trigger_point")
    print(type(trigger_point))

    # Check if the wallet exists
    existing_wallets = (
        supabase.table("Wallets")
        .select()
        .eq("chat_id", context.user_data["chat_id"])
        .eq("wallet_address", wallet_address)
        .execute()
    )
    print(existing_wallets)

    if not existing_wallets.data:
        # Wallet does not exist, insert new record
        data = (
            supabase.table("Wallets")
            .insert(
                {
                    "chat_id": context.user_data["chat_id"],
                    "wallet_name": wallet_name,
                    "wallet_address": wallet_address,
                }
            )
            .execute()
        )
        print("Wallet added")
    else:
        print("Wallet already exists")

    # data = (
    #     supabase.table("Contracts")
    #     .insert(
    #         {
    #             "wallet_address": wallet_address,
    #             "blockchain": blockchain,
    #             "contract_address": contract_address,
    #             "token_symbol": symbol,
    #             "trigger_point": trigger_point,
    #             "balance": None,
    #         }
    #     )
    #     .execute()
    # )

    message = await tracked_wallet_setup_message(
        wallet_name,
        blockchain,
        wallet_address,
        symbol,
        contract_address,
        trigger_point,
        language,
    )

    await context.bot.send_message(
        chat_id=context.user_data["chat_id"],
        text=message,
        reply_markup=await back_to_to_main_keyboard(context.user_data["language"]),
    )


############################ Settings Menus ####################################


async def settings_menu(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=await settings_message(language),
        reply_markup=await settings_menu_keyboard(language),
    )


async def language_selection_menu(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=await language_selection_message(language),
        reply_markup=await language_keyboard(language),
    )


async def language_selection(update, context):
    query = update.callback_query
    selected_language = query.data
    context.user_data["language"] = selected_language
    await query.answer()
    await query.edit_message_text(
        text=await language_selection_message(context.user_data["language"]),
        reply_markup=await language_keyboard(context.user_data["language"]),
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
    application.add_handler(
        CallbackQueryHandler(language_selection, pattern=r"^(en|es|fr)$")
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
