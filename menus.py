from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def main_menu_keyboard():
    # Define the main menu options
    options = [
        InlineKeyboardButton("🚀 Track", callback_data="m1"),
        InlineKeyboardButton("❌ Untrack", callback_data="m2"),
        InlineKeyboardButton("📋 Wallets", callback_data="m3"),
        InlineKeyboardButton("⚙️ Settings", callback_data="m4"),
        InlineKeyboardButton("❓ Help", callback_data="m5"),
    ]

    # Maximum options per row
    max_options_per_row = 2

    # Divide options into rows
    keyboard = []
    for i in range(0, len(options), max_options_per_row):
        keyboard.append(options[i : i + max_options_per_row])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def language_keyboard() -> InlineKeyboardMarkup:
    options = [
        [
            InlineKeyboardButton("🏴󠁧󠁢󠁥󠁮󠁧󠁿 English", callback_data="en"),
            InlineKeyboardButton("🇫🇷 Français", callback_data="fr"),
            InlineKeyboardButton("🏠 Main menu", callback_data="main"),
        ]
    ]

    # Maximum options per row
    max_options_per_row = 2

    # Divide options into rows
    keyboard = []
    for i in range(0, len(options), max_options_per_row):
        keyboard.append(options[i : i + max_options_per_row])

    return InlineKeyboardMarkup(keyboard)


async def settings_menu_keyboard():
    # Define the main menu options
    options = [
        InlineKeyboardButton("🌏 Language", callback_data="m1"),
        InlineKeyboardButton("🏠 Main menu", callback_data="main"),
    ]

    # Maximum options per row
    max_options_per_row = 2

    # Divide options into rows
    keyboard = []
    for i in range(0, len(options), max_options_per_row):
        keyboard.append(options[i : i + max_options_per_row])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
