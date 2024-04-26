from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def main_menu_keyboard():
    # Define the main menu options
    options = [
        InlineKeyboardButton("🚀 Track", callback_data="add_wallet_menu"),
        InlineKeyboardButton("❌ Untrack", callback_data="remove_wallet_menu"),
        InlineKeyboardButton("📋 Wallets", callback_data="list_wallets"),
        InlineKeyboardButton("⚙️ Settings", callback_data="settings_menu"),
        InlineKeyboardButton("❓ Help", callback_data="help_menu"),
    ]

    # Maximum options per row
    max_options_per_row = 2

    # Divide options into rows
    keyboard = []
    for i in range(0, len(options), max_options_per_row):
        keyboard.append(options[i : i + max_options_per_row])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def settings_menu_keyboard():
    # Define the main menu options
    options = [
        InlineKeyboardButton("🌏 Language", callback_data="language_menu"),
        InlineKeyboardButton("🏠 Main menu", callback_data="main"),
    ]

    # Maximum options per row
    max_options_per_row = 2

    # Divide options into rows
    keyboard = []
    for i in range(0, len(options), max_options_per_row):
        keyboard.append(options[i : i + max_options_per_row])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def language_keyboard():
    # Define the main menu options
    options = [
        InlineKeyboardButton("🏴󠁧󠁢󠁥󠁮󠁧󠁿 English", callback_data="en"),
        InlineKeyboardButton("🇫🇷 Français", callback_data="fr"),
        InlineKeyboardButton("🏠 Main menu", callback_data="main"),
    ]

    # Maximum options per row
    max_options_per_row = 2

    # Divide options into rows
    keyboard = []
    for i in range(0, len(options), max_options_per_row):
        keyboard.append(options[i : i + max_options_per_row])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def add_wallet_keyboard():
    # Define the main menu options
    options = [
        InlineKeyboardButton("🌏 Test 1", callback_data="test"),
        InlineKeyboardButton("🌏 Test 2", callback_data="test2"),
        InlineKeyboardButton("🏠 Main menu", callback_data="main"),
    ]

    # Maximum options per row
    max_options_per_row = 2

    # Divide options into rows
    keyboard = []
    for i in range(0, len(options), max_options_per_row):
        keyboard.append(options[i : i + max_options_per_row])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def back_to_to_main_keyboard():
    # Define the main menu options
    options = [
        InlineKeyboardButton("🏠 Main menu", callback_data="main"),
    ]

    # Maximum options per row
    max_options_per_row = 2

    # Divide options into rows
    keyboard = []
    for i in range(0, len(options), max_options_per_row):
        keyboard.append(options[i : i + max_options_per_row])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
