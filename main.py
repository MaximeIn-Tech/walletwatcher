import asyncio
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
from wallets import *

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

############################ Utilities  #########################################

async def delete_message_after_delay(bot, chat_id, message_id, delay):
    await asyncio.sleep(delay)
    await bot.delete_message(chat_id=chat_id, message_id=message_id)


############################ Bot Menus #########################################

async def start(update, context):
    try:
        language = update.effective_user.language_code
        context.user_data["language"] = language

        context.user_data["chat_id"] = update.effective_chat.id
        context.user_data["name"] = update.message.from_user.first_name

        # Check if the user already exists in the Users table
        existing_user = (
            supabase.table("Users")
            .select("*")
            .eq("chat_id", context.user_data["chat_id"])
            .execute()
        )

        if not existing_user.data:
            # User does not exist, insert new record
            data, count = (
                supabase.table("Users")
                .insert(
                    {
                        "chat_id": context.user_data["chat_id"],
                        "language": context.user_data["language"],
                        "subscription": "Free",
                    }
                )
                .execute()
            )
            logger.info(f"User {context.user_data['chat_id']} added.")
        else:
            # User exists, update the language if not available in the database
            if existing_user.data[0]['language'] is None:
                (
                    supabase.table("Users")
                    .update({"language": context.user_data["language"]})
                    .eq("chat_id", context.user_data["chat_id"])
                    .execute()
                )
                logger.info(f"Language updated for user {context.user_data['chat_id']}.")

        # Use the language from the database if available, else fallback to Telegram language
        user_language = (
            existing_user.data[0]['language']
            if existing_user.data and existing_user.data[0]['language']
            else language
        )

        # Reply to the user
        await update.message.reply_text(
            await main_menu_message(context.user_data["name"], user_language),
            reply_markup=await main_menu_keyboard(user_language),
        )
    except Exception as e:
        logger.error("An error occurred:", e)


async def main_menu(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
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
        text=await help_menu(language),
        reply_markup=await help_menu_keyboard(language),
    )

async def handle_privacy(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=await privacy_message(language),
        reply_markup=await back_to_help_menu(language),
    )
    
async def handle_donation(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=await donation_message(language),
        reply_markup=await back_to_help_menu(language),
    )

async def handle_data_collection(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=await data_collection_message(language),
        reply_markup=await back_to_help_menu(language),
    )

############################ Wallets Section #########################################

async def show_wallets(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    chat_id = query.message.chat_id

    # Fetch wallets associated with the user from the database
    user_wallets = await fetch_wallets_user(chat_id)

    if user_wallets.count > 0:
        wallets_data = sorted(user_wallets.data, key=lambda x: x["wallet_name"].lower()) 
        buttons = []

        # Generate buttons two by two
        for i in range(0, len(wallets_data), 2):
            row = []
            for j in range(2):
                if i + j < len(wallets_data):
                    wallet = wallets_data[i + j]
                    row.append(InlineKeyboardButton(wallet["wallet_name"], callback_data=f"wallet_{wallet['wallet_address']}"))
            buttons.append(row)

        buttons.append([InlineKeyboardButton("🔙", callback_data="main_menu")])

        reply_markup = InlineKeyboardMarkup(buttons)

        await query.answer()
        await query.edit_message_text(
            text=await wallets_found(language),
            reply_markup=reply_markup,
        )
    else:
        # If user doesn't have any wallets, inform them
        await query.answer()
        await query.edit_message_text(
            text=await no_wallets_found(language),
            reply_markup=await back_to_to_main_keyboard(language),
        )

async def handle_wallet_selection(update, context):
    chat_id=update.effective_chat.id
    language = await get_language_for_chat_id(chat_id)
    query = update.callback_query
    wallet_address = query.data.split("_")[1]  # Extract wallet address from callback data

    # Fetch all setups associated with the selected wallet address
    setups = await fetch_setup_wallet(wallet_address, chat_id)
    alert = await alert_text(language)

    if setups.data:
        # If setups are found, format them and send to the user
        alert = await alert_text(language)
        formatted_message = generate_formatted_setups(setups, alert, language)

        await query.answer()
        await query.edit_message_text(
            text=await setups_found(language, formatted_message, wallet_address),
            reply_markup=await back_to_list_wallets(language),
        )
    else:
        # If no setups are found, inform the user
        await query.answer()
        await query.edit_message_text(
            text=await no_setups_found(language),
            reply_markup=await back_to_list_wallets(language),
        )

########################## Remove Wallet #######################################

async def generate_setup_buttons_and_alerts(setups, language, alert):
    buttons = []
    alerts_to_display = []
    alert = await alert_text(language)
    row = []
    for index, setup in enumerate(setups.data, start=1):
        row.append(InlineKeyboardButton(f"{alert} {index}", callback_data=f"delete_setup_{setup['id']}"))
        if len(row) == 2:  # Two buttons per row
            buttons.append(row)
            row = []  # Reset the row for the next pair of buttons
        if language == "fr":
            alerts_to_display.append(
                f"""\n{alert} {index}:
Blockchain : {setup["blockchain"]}"""
                + (f"\nToken : {setup['token_symbol']}" if setup['token_symbol'] is not None else '')
                + (f"\nContract Address : {setup['contract_address']}" if setup['contract_address'] is not None else '')
                + (f"\nSeuil de déclenchement : {setup['trigger_point']}" if setup['trigger_point'] is not None else '')
                + (f"\nSolde actuelle : {setup['balance']} {setup['token_symbol']}" if setup['balance'] is not None else '')
            )
        elif language == "es":
            alerts_to_display.append(
                f"""\n{alert} {index}:
Blockchain: {setup["blockchain"]}"""
                + (f"\nToken: {setup['token_symbol']}" if setup['token_symbol'] is not None else '')
                + (f"\nDirección del Contrato: {setup['contract_address']}" if setup['contract_address'] is not None else '')
                + (f"\nPunto de Activación: {setup['trigger_point']}" if setup['trigger_point'] is not None else '')
                + (f"\nSaldo: {setup['balance']} {setup['token_symbol']}" if setup['balance'] is not None else '')
            )
        # Add more language conditions as needed
        else:
            # Default to English if language not specified or recognized
            alerts_to_display.append(
                f"""\n{alert} {index}:
Blockchain: {setup["blockchain"]}"""
                + (f"\nToken: {setup['token_symbol']}" if setup['token_symbol'] is not None else '')
                + (f"\nContract Address: {setup['contract_address']}" if setup['contract_address'] is not None else '')
                + (f"\nTrigger Point: {setup['trigger_point']}" if setup['trigger_point'] is not None else '')
                + (f"\nCurrent balance: {setup['balance']} {setup['token_symbol']}" if setup['balance'] is not None else '')
            )
    # Add the last row if it has any buttons
    if row:
        buttons.append(row)
    if language == "fr":
        cancel_text = "Annuler"
    elif language == "es":
        cancel_text = "Cancelar"
    else:
        cancel_text = "Cancel"

    buttons.append([InlineKeyboardButton(cancel_text, callback_data="remove_wallet_menu")])
    reply_markup = InlineKeyboardMarkup(buttons)
    formatted_setups = "\n".join(alerts_to_display)
    
    return reply_markup, formatted_setups



async def untrack_menu(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    await query.answer()

    # Fetch all wallets associated with the user
    user_wallets = await fetch_wallets_user(update.effective_chat.id)

    if user_wallets.count > 0:
        wallets_data = sorted(user_wallets.data, key=lambda x: x["wallet_name"].lower())
        buttons = []
        row = []  # Initialize row for buttons

        # Generate buttons for each wallet
        for wallet in wallets_data:
            # Add button to current row
            row.append(InlineKeyboardButton(wallet["wallet_name"], callback_data=f"untrack_wallet_{wallet['wallet_address']}"))
            
            # If row is full (2 buttons), add it to buttons and start a new row
            if len(row) == 2:
                buttons.append(row)
                row = []

        # If there are remaining buttons in the last row, add it to buttons
        if row:
            buttons.append(row)

        buttons.append([InlineKeyboardButton("🔙", callback_data="main_menu")])

        reply_markup = InlineKeyboardMarkup(buttons)

        await query.edit_message_text(
            text=await wallets_found_track(language),
            reply_markup=reply_markup,
        )
    else:
        await query.edit_message_text(
            text=await no_wallets_found(language),
            reply_markup=await back_to_to_main_keyboard(language),
        )


async def handle_untrack_wallet_selection(update, context):
    chat_id = update.effective_chat.id
    language = await get_language_for_chat_id(chat_id)
    query = update.callback_query
    wallet_address = query.data.split("_")[2]  # Extract wallet address
    context.user_data['wallet_address_delete'] = wallet_address

    # Fetch all setups associated with the selected wallet
    setups = await fetch_setup_wallet(wallet_address, chat_id)
    alert = await alert_text(language)
    alert_choice_1 = await setup_to_delete_1(language)
    alert_choice_2 = await setup_to_delete_2(language)

    if setups.data:
        reply_markup, formatted_setups = await generate_setup_buttons_and_alerts(setups, language, alert)

        await query.answer()
        await query.edit_message_text(
            text=f"{alert_choice_1}\n{formatted_setups}\n\n{alert_choice_2}",
            reply_markup=reply_markup,
        )

        return reply_markup
    else:
        await query.answer()
        await query.edit_message_text(
            text=await no_setups_found(language),
            reply_markup=await back_to_list_wallets(language),
        )
        return None

async def delete_alert(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    chat_id = update.effective_chat.id
    query = update.callback_query
    setup_id = int(query.data.split("_")[2])
    await remove_setup_from_db(setup_id)

    # Fetch setups associated with the wallet again
    wallet_address = context.user_data['wallet_address_delete']
    setups = await fetch_setup_wallet(wallet_address, chat_id)

    alert = await alert_text(language)
    alert_choice_1 = await setup_to_delete_1(language)
    alert_choice_2 = await setup_to_delete_2(language)

    if setups.data:
        reply_markup, formatted_setups = await generate_setup_buttons_and_alerts(setups, language, alert)

        await query.edit_message_text(
            text=f"{alert_choice_1}\n\n{formatted_setups}\n\n{alert_choice_2}",
            reply_markup=reply_markup,
        )
    else:
        await query.edit_message_text(
            text=await setup_deletion_success(language),  # or any other appropriate message
            reply_markup=await back_to_remove_wallet(language)
        )


async def delete_all(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
            text = await remove_all_data(language),
            reply_markup=await remove_all_data_keyboard(language),
        )
    
async def handle_deletion_delete_all(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    chat_id = update.effective_chat.id
    query = update.callback_query
    user_response = query.data
    if user_response == 'yes_delete':
        await remove_all_from_db(chat_id)
        await query.edit_message_text(
            text=await all_data_removed(language),
            reply_markup=await back_to_to_main_keyboard(language),
        )
    elif user_response == 'no_delete':
        # User canceled deletion, you can handle this according to your needs
        await query.answer("Deletion canceled.")
        await query.message.delete()
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=await main_menu_message(context.user_data["name"], language),
            reply_markup=await main_menu_keyboard(language)
        )
    else:
        # Handle unexpected user response
        await query.answer("Invalid response. Please use the provided buttons.")
    
############################ Add Track #########################################
"""
TODO:
- Add more information in the help menu:
    - Where is the data taken.
"""

# STEP 1 : Handle blockchain selection

async def add_wallet(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    context.user_data["chat_id"] = query.message.chat_id
    await query.answer()
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=await blockchain_choice_message(language),
        reply_markup=await blockchain_keyboard(),
    )



async def track_sub_menu_1(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    context.user_data["chat_id"] = query.message.chat_id
    
    # Fetch wallets associated with the user from the database
    user_wallets = await fetch_wallets_user(context.user_data["chat_id"])

    user_setups = await fetch_setups_user(context.user_data["chat_id"])

    if  user_setups.count <=5:
        if user_wallets.count > 0:
            # User has existing wallets, display them in a menu
            wallets_data = sorted(user_wallets.data, key=lambda x: x["wallet_name"].lower()) 
            buttons = []

            # Generate buttons two by two
            for i in range(0, len(wallets_data), 2):
                row = []
                for j in range(2):
                    if i + j < len(wallets_data):
                        wallet = wallets_data[i + j]
                        row.append(InlineKeyboardButton(wallet["wallet_name"], callback_data=f"add_wallet_{wallet['wallet_address']}"))
                buttons.append(row)

            buttons.append([InlineKeyboardButton("➕", callback_data="add_new_wallet")])

            reply_markup = InlineKeyboardMarkup(buttons)

            await query.answer()
            await context.bot.send_message(chat_id=update.effective_chat.id,text=await wallets_found_track(language), reply_markup=reply_markup)
        else:
            # If user doesn't have any wallets, prompt them to add a new wallet
            await query.answer()
            await context.bot.send_message(chat_id=update.effective_chat.id,text = await blockchain_choice_message(language), reply_markup=await blockchain_keyboard())
    else:
        message = await context.bot.send_message(chat_id=update.effective_chat.id,text = await too_many_setups(language))

        # Use ensure_future to asynchronously delete the message after a delay
        asyncio.ensure_future(delete_message_after_delay(context.bot, update.effective_chat.id, message.message_id, delay=10))

async def handle_wallet_selection_for_add(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    wallet_address = query.data.split("_")[2]
    # Fetch the wallet name associated with the selected wallet address
    wallet_response = await fetch_wallet_address(wallet_address)
    if wallet_response.data:
        wallet_data = wallet_response.data[0]
        wallet_name = wallet_data["wallet_name"]
    else:
        # Handle the case where wallet data is not found
        wallet_name = "Unknown Wallet"

    # Store the selected wallet address and name in the user data
    context.user_data["wallet_address"] = wallet_address
    context.user_data["wallet_name"] = wallet_name

    # Proceed with the new track creation process
    # You can prompt the user for additional information or proceed accordingly
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
    
    if "wallet_address" in context.user_data:
        await naming_wallet_selection(update, context)
    else:
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
    language = await get_language_for_chat_id(update.effective_chat.id)
    if context.user_data.get("is_entering_wallet_name", False):
        await handle_wallet_name(update, context)
    elif context.user_data.get("is_entering_trigger_point", False):
        await handle_trigger_point(update, context)
    elif context.user_data.get("is_entering_contract_address", False):
        await handle_contract_address(update, context)
    elif "blockchain" in context.user_data:
        # Only proceed with handling wallet address if blockchain key is present
        await handle_wallet_address(update, context)
    else:
        # Handle other cases or send a message informing the user
        message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text= await use_buttons(language),
        )

        user_input_message_id = update.message.message_id
        # Delete the message after x seconds (e.g., 10 seconds)
        await asyncio.sleep(3)
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=message.message_id
        )
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=user_input_message_id
        )


# STEP 3 : Name the wallet.
async def naming_wallet_selection(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    selected_option = query.data
    await query.answer()

    if "wallet_name" in context.user_data:
        await select_token_symbol(update, context)
    else:
        if selected_option == "yes":
            context.user_data["is_entering_wallet_name"] = True
            await context.bot.send_message(
                chat_id=context.user_data["chat_id"],
                text=await naming_wallet(language),
            )
        elif selected_option == "no":
            context.user_data["wallet_name"] = "None"
            await select_token_symbol(update, context)

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
            # Now you can use selected_symbol and contract_address as needed
            # For example, store them in user_data
            context.user_data["selected_symbol"] = selected_symbol
            context.user_data["contract_address"] = contract_address
            context.user_data["blockchain"] = selected_blockchain

            selected_blockchain = selected_blockchain.upper()
            # Check if the selected blockchain is Theta and the selected token is "Stake Watch"
            if (
                selected_blockchain == "THETA"
                and selected_symbol == "Stake Watch"
            ):
                await context.bot.send_message(
                    chat_id=update.callback_query.message.chat_id,
                    text=await stake_message(language),
                    reply_markup=await back_to_to_main_keyboard(language),
                )
                await prompt_tracked_wallet(update, context)
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
    symbol = None
    if symbol != "Stake Watch":
        await context.bot.send_message(
            chat_id=context.user_data["chat_id"],
            text=await trigger_point_selection(language),
            parse_mode="HTML",
        )
        context.user_data["is_entering_trigger_point"] = True
    else:
        await prompt_tracked_wallet(update, context)

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
    await prompt_tracked_wallet(update, context)

# COMPLETED:
#TODO : Fetch the initial balance and add it to the setup
async def prompt_tracked_wallet(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    blockchain = context.user_data.get("blockchain").upper()
    wallet_address = context.user_data.get("wallet_address")
    wallet_name = context.user_data.get("wallet_name")
    symbol = context.user_data.get("selected_symbol")
    contract_address = context.user_data.get("contract_address")
    trigger_point = context.user_data.get("trigger_point")
    print(symbol)
    if symbol != "Stake Watch":
        print(wallet_address, contract_address)
        balance = fetch_wallet_balance(blockchain, symbol, wallet_address, contract_address)
        print(balance)
        if balance != None:
            balance = round(balance, 2)
        stake = None
    else:
        stake = fetch_theta_stake(wallet_address)
        stake = stake["body"]
        print(stake)
        balance = None

    if symbol is None:
        symbol = fetch_token_symbol_for_contract(blockchain, contract_address)

    # Check if the wallet exists
    existing_wallets = (
        supabase.table("Wallets")
        .select("*")
        .eq("chat_id", context.user_data["chat_id"])
        .eq("wallet_address", wallet_address)
        .execute()
    )
    count = await fetch_wallets_user(context.user_data["chat_id"])
    logger.info (f"User {context.user_data["chat_id"]} has {count.count} wallets in the db")

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
        logger.info(f"Wallet for {context.user_data["chat_id"]} added")
    else:
        logger.info(f"Wallet of {context.user_data["chat_id"]} already exists")

    data = (
        supabase.table("Setups")
        .insert(
            {
                "chat_id": context.user_data["chat_id"],
                "wallet_address": wallet_address,
                "blockchain": blockchain,
                "contract_address": contract_address,
                "token_symbol": symbol,
                "trigger_point": trigger_point,
                "balance": balance,
                "stake_data": stake,
            }
        )
        .execute()
    )


    count = await fetch_setups_user(context.user_data["chat_id"])
    logger.info (f"User {context.user_data["chat_id"]} has {count.count} contracts in the db")
    blockchain = blockchain.capitalize()
    wallet_address = wallet_address.lower()
    message = await tracked_wallet_setup_message(
        wallet_name,
        blockchain,
        wallet_address,
        symbol,
        contract_address,
        trigger_point,
        balance,
        stake,
        language,
    )

    await context.bot.send_message(
        chat_id=context.user_data["chat_id"],
        text=message,
        reply_markup=await back_to_to_main_keyboard(language),
    )

    context.user_data.clear()

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
    chat_id = update.effective_chat.id
    query = update.callback_query
    selected_language = query.data
    supabase = connect_to_database()
    user_response = (
            supabase.table("Users")
            .update({"language": selected_language})
            .eq("chat_id", chat_id)
            .execute()
        )
    context.user_data["language"] = selected_language
    
    await query.answer()
    await query.edit_message_text(
        text=await language_selection_message(context.user_data["language"]),
        reply_markup=await language_keyboard(context.user_data["language"]),
    )

############################ Subscriptions ####################################

async def subscription_menu(update, context):
    language = await get_language_for_chat_id(update.effective_chat.id)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=await subscription_explanation(language),
        reply_markup=await back_to_settings_menu(language),
    )


if __name__ == "__main__":
    print("Starting bot ...")
    application = Application.builder().token(token).build()

    ############################ BUTTON INTERACTION HANDLERS ###################
    ############################ Main Menu Handlers ############################

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", start))
    application.add_handler(CallbackQueryHandler(main_menu, pattern="main"))
    application.add_handler(CallbackQueryHandler(help, pattern="help_menu"))
    application.add_handler(CallbackQueryHandler(show_wallets, pattern="list_wallets"))
    application.add_handler(CallbackQueryHandler(untrack_menu, pattern="remove_wallet_menu"))
    application.add_handler(CallbackQueryHandler(delete_all, pattern="delete_all"))
    application.add_handler(CallbackQueryHandler(handle_deletion_delete_all, pattern=r"^(yes_delete|no_delete)$"))
    application.add_handler(
    CallbackQueryHandler(handle_wallet_selection, pattern=r"^wallet_")
)

    ############################ Delete Section ################################

    application.add_handler(
    CallbackQueryHandler(handle_untrack_wallet_selection, pattern=r"^untrack_wallet_")
)
    application.add_handler(
    CallbackQueryHandler(delete_alert, pattern=r"^delete_setup_\d+$")
)

    ############################ Add Track Handlers ############################
    application.add_handler(
        CallbackQueryHandler(track_sub_menu_1, pattern="track_menu")
    )
    application.add_handler(
        CallbackQueryHandler(add_wallet, pattern="add_new_wallet")
    )
    application.add_handler(
        CallbackQueryHandler(blockchain_selection, pattern=r"^(theta|bsc|eth)$")
    )
    application.add_handler(
    CallbackQueryHandler(handle_wallet_selection_for_add, pattern=r"add_wallet_")
)

    ############################ Setting Handlers ##############################
    application.add_handler(
        CallbackQueryHandler(settings_menu, pattern="settings_menu")
    )
    application.add_handler(
        CallbackQueryHandler(subscription_menu, pattern="subscriptions_menu")
    )
    
    application.add_handler(
        CallbackQueryHandler(language_selection_menu, pattern="language_menu")
    )
    application.add_handler(
        CallbackQueryHandler(language_selection, pattern=r"^(en|es|fr)$")
    )
    application.add_handler(
        CallbackQueryHandler(handle_privacy, pattern="privacy")
    )
    application.add_handler(
        CallbackQueryHandler(handle_donation, pattern="donation")
    )
    application.add_handler(
        CallbackQueryHandler(handle_data_collection, pattern="data_collection")
    )


    ############################ Naming Wallet Handlers #########################################
    application.add_handler(
        CallbackQueryHandler(naming_wallet_selection, pattern=r"^(yes|no)$")
    )

    application.add_handler(CallbackQueryHandler(handle_selected_token))

    ############################ MESSAGE HANDLERS ############################
    ############################ Add Track Handlers ############################
    application.add_handler(MessageHandler(filters.Text(), handle_messages))

    print("Start polling ...")

    application.run_polling(allowed_updates=Update.ALL_TYPES)
