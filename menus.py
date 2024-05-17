from telegram import InlineKeyboardButton, InlineKeyboardMarkup

############################ Main Menu #########################################


async def main_menu_keyboard(user_language: str) -> InlineKeyboardMarkup:

    english_options = [
        InlineKeyboardButton("🚀 Add an alert", callback_data="track_menu"),
        InlineKeyboardButton("❌ Delete an alert", callback_data="remove_wallet_menu"),
        InlineKeyboardButton("📜 Wallets", callback_data="list_wallets"),
        InlineKeyboardButton("⚙️ Settings", callback_data="settings_menu"),
        InlineKeyboardButton("❓ Help", callback_data="help_menu"),
    ]

    french_options = [
        InlineKeyboardButton("🚀 Ajouter une alerte", callback_data="track_menu"),
        InlineKeyboardButton(
            "❌ Supprimer une alerte", callback_data="remove_wallet_menu"
        ),
        InlineKeyboardButton("📜 Portefeuilles", callback_data="list_wallets"),
        InlineKeyboardButton("⚙️ Paramètres", callback_data="settings_menu"),
        InlineKeyboardButton("❓ Aide", callback_data="help_menu"),
    ]

    spanish_options = [
        InlineKeyboardButton("🚀 Agregar una alerta", callback_data="track_menu"),
        InlineKeyboardButton(
            "❌ Eliminar una alerta", callback_data="remove_wallet_menu"
        ),
        InlineKeyboardButton("📜 Carteras", callback_data="list_wallets"),
        InlineKeyboardButton("⚙️ Configuración", callback_data="settings_menu"),
        InlineKeyboardButton("❓ Ayuda", callback_data="help_menu"),
    ]

    if user_language == "fr":
        buttons = french_options
    elif user_language == "es":
        buttons = spanish_options
    else:
        buttons = english_options

    # Maximum options per row
    max_options_per_row = 2

    # Divide options into rows
    keyboard = []
    for i in range(0, len(buttons), max_options_per_row):
        keyboard.append(buttons[i : i + max_options_per_row])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def help_menu_keyboard(user_language: str) -> InlineKeyboardMarkup:

    english_options = [
        InlineKeyboardButton("🔓 Privacy", callback_data="privacy"),
        InlineKeyboardButton("📊 Data Collection", callback_data="data_collection"),
        InlineKeyboardButton("🌱 Donation", callback_data="donation"),
    ]

    french_options = [
        InlineKeyboardButton("🔓 Confidentialité", callback_data="privacy"),
        InlineKeyboardButton("📊 Collecte de données", callback_data="data_collection"),
        InlineKeyboardButton("🌱 Donation", callback_data="donation"),
    ]

    spanish_options = [
        InlineKeyboardButton("🔓 Privacidad", callback_data="privacy"),
        InlineKeyboardButton(
            "📊 Recolección de datos", callback_data="data_collection"
        ),
        InlineKeyboardButton("🌱 Donación", callback_data="donation"),
    ]

    main_menu_button_texts = {
        "en": "🏠 Main menu",
        "fr": "🏠 Menu principal",
        "es": "🏠 Menú principal",
    }

    main_menu_button = InlineKeyboardButton(
        main_menu_button_texts.get(user_language, "🏠 Main menu"), callback_data="main"
    )

    if user_language == "fr":
        buttons = french_options
    elif user_language == "es":
        buttons = spanish_options
    else:
        buttons = english_options

    # Maximum options per row
    max_options_per_row = 2

    # Divide options into rows
    keyboard = []
    for i in range(0, len(buttons), max_options_per_row):
        keyboard.append(buttons[i : i + max_options_per_row])

    # Add the "back" button and the "main menu" button as the last row
    keyboard.append([main_menu_button])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def back_to_help_menu(user_language: str) -> InlineKeyboardMarkup:

    english_options = [
        [
            InlineKeyboardButton("🔙", callback_data="help_menu"),
        ],
        [InlineKeyboardButton("🏠 Main menu", callback_data="main")],
    ]

    french_options = [
        [
            InlineKeyboardButton("🔙", callback_data="help_menu"),
        ],
        [InlineKeyboardButton("🏠 Menu principal", callback_data="main")],
    ]

    spanish_options = [
        [
            InlineKeyboardButton("🔙", callback_data="help_menu"),
        ],
        [InlineKeyboardButton("🏠 Menú principal", callback_data="main")],
    ]

    if user_language == "fr":
        buttons = french_options
    elif user_language == "es":
        buttons = spanish_options
    else:
        buttons = english_options

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def back_to_to_main_keyboard(user_language: str) -> InlineKeyboardMarkup:

    english_options = [
        [InlineKeyboardButton("🏠 Main menu", callback_data="main")],
    ]

    french_options = [
        [InlineKeyboardButton("🏠 Menu principal", callback_data="main")],
    ]

    spanish_options = [
        [InlineKeyboardButton("🏠 Menú principal", callback_data="main")],
    ]

    if user_language == "fr":
        buttons = french_options
    elif user_language == "es":
        buttons = spanish_options
    else:
        buttons = english_options

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def back_to_list_wallets(user_language: str) -> InlineKeyboardMarkup:

    english_options = [
        [
            InlineKeyboardButton("🔙", callback_data="list_wallets"),
        ],
        [InlineKeyboardButton("🏠 Main menu", callback_data="main")],
    ]

    french_options = [
        [
            InlineKeyboardButton("🔙", callback_data="list_wallets"),
        ],
        [InlineKeyboardButton("🏠 Menu principal", callback_data="main")],
    ]

    spanish_options = [
        [
            InlineKeyboardButton("🔙", callback_data="list_wallets"),
        ],
        [InlineKeyboardButton("🏠 Menú principal", callback_data="main")],
    ]

    if user_language == "fr":
        buttons = french_options
    elif user_language == "es":
        buttons = spanish_options
    else:
        buttons = english_options

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def back_to_remove_wallet(user_language: str) -> InlineKeyboardMarkup:

    english_options = [
        [
            InlineKeyboardButton("🔙", callback_data="remove_wallet_menu"),
        ],
        [InlineKeyboardButton("🏠 Main menu", callback_data="main")],
    ]

    french_options = [
        [
            InlineKeyboardButton("🔙", callback_data="remove_wallet_menu"),
        ],
        [InlineKeyboardButton("🏠 Menu principal", callback_data="main")],
    ]

    spanish_options = [
        [
            InlineKeyboardButton("🔙", callback_data="remove_wallet_menu"),
        ],
        [InlineKeyboardButton("🏠 Menú principal", callback_data="main")],
    ]

    if user_language == "fr":
        buttons = french_options
    elif user_language == "es":
        buttons = spanish_options
    else:
        buttons = english_options

    return InlineKeyboardMarkup(inline_keyboard=buttons)


############################ Settings Menus #########################################


async def settings_menu_keyboard(user_language: str) -> InlineKeyboardMarkup:

    english_options = [
        InlineKeyboardButton("🌏 Language", callback_data="language_menu"),
        InlineKeyboardButton("💳 Subscriptions", callback_data="subscriptions_menu"),
        InlineKeyboardButton("❌ Delete all data", callback_data="delete_all"),
        InlineKeyboardButton("🏠 Main menu", callback_data="main"),
    ]

    french_options = [
        InlineKeyboardButton("🌏 Langue", callback_data="language_menu"),
        InlineKeyboardButton("💳 Abonnements", callback_data="subscriptions_menu"),
        InlineKeyboardButton("❌ Supprimer mes données", callback_data="delete_all"),
        InlineKeyboardButton("🏠 Menu principal", callback_data="main"),
    ]

    spanish_options = [
        InlineKeyboardButton("🌏 Idioma", callback_data="language_menu"),
        InlineKeyboardButton("💳 Suscripciones", callback_data="subscriptions_menu"),
        InlineKeyboardButton("❌ Eliminar mis datos", callback_data="delete_all"),
        InlineKeyboardButton("🏠 Menú principal", callback_data="main"),
    ]

    if user_language == "fr":
        buttons = french_options
    elif user_language == "es":
        buttons = spanish_options
    else:
        buttons = english_options

    # Maximum options per row
    max_options_per_row = 2

    # Divide options into rows
    keyboard = []
    for i in range(0, len(buttons), max_options_per_row):
        keyboard.append(buttons[i : i + max_options_per_row])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def language_keyboard(user_language: str) -> InlineKeyboardMarkup:

    english_options = (
        [
            InlineKeyboardButton("🏴󠁧󠁢󠁥󠁮󠁧󠁿 English", callback_data="en"),
            InlineKeyboardButton("🇫🇷 French", callback_data="fr"),
        ],
        [
            InlineKeyboardButton("🇪🇸 Spanish", callback_data="es"),
        ],
        [
            InlineKeyboardButton("🔙", callback_data="settings_menu"),
            InlineKeyboardButton("🏠 Main Menu", callback_data="main"),
        ],
    )

    french_options = (
        [
            InlineKeyboardButton("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Anglais", callback_data="en"),
            InlineKeyboardButton("🇫🇷 Français", callback_data="fr"),
        ],
        [
            InlineKeyboardButton("🇪🇸 Espagnol", callback_data="es"),
        ],
        [
            InlineKeyboardButton("🔙", callback_data="settings_menu"),
            InlineKeyboardButton("🏠 Menu principal", callback_data="main"),
        ],
    )

    spanish_options = (
        [
            InlineKeyboardButton("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglés", callback_data="en"),
            InlineKeyboardButton("🇫🇷 Francés", callback_data="fr"),
        ],
        [
            InlineKeyboardButton("🇪🇸 Español", callback_data="es"),
        ],
        [
            InlineKeyboardButton("🔙", callback_data="settings_menu"),
            InlineKeyboardButton("🏠 Menú principal", callback_data="main"),
        ],
    )

    if user_language == "fr":
        buttons = french_options
    elif user_language == "es":
        buttons = spanish_options
    else:
        buttons = english_options

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def back_to_settings_menu(user_language: str) -> InlineKeyboardMarkup:

    english_options = [
        [
            InlineKeyboardButton("🔙", callback_data="settings_menu"),
        ],
        [InlineKeyboardButton("🏠 Main menu", callback_data="main")],
    ]

    french_options = [
        [
            InlineKeyboardButton("🔙", callback_data="settings_menu"),
        ],
        [InlineKeyboardButton("🏠 Menu principal", callback_data="main")],
    ]

    spanish_options = [
        [
            InlineKeyboardButton("🔙", callback_data="settings_menu"),
        ],
        [InlineKeyboardButton("🏠 Menú principal", callback_data="main")],
    ]

    if user_language == "fr":
        buttons = french_options
    elif user_language == "es":
        buttons = spanish_options
    else:
        buttons = english_options

    return InlineKeyboardMarkup(inline_keyboard=buttons)


############################ Add Track Menus #########################################


async def blockchain_keyboard():
    # Define the main menu options
    options = [
        InlineKeyboardButton("THETA", callback_data="theta"),
        InlineKeyboardButton("ETH", callback_data="eth"),
        InlineKeyboardButton("BSC", callback_data="bsc"),
    ]

    # Maximum options per row
    max_options_per_row = 1

    # Divide options into rows
    keyboard = []
    for i in range(0, len(options), max_options_per_row):
        keyboard.append(options[i : i + max_options_per_row])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def naming_wallet_keyboard(user_language: str) -> InlineKeyboardMarkup:

    english_options = [
        InlineKeyboardButton("Yes", callback_data="yes"),
        InlineKeyboardButton("No", callback_data="no"),
    ]

    french_options = [
        InlineKeyboardButton("Oui", callback_data="yes"),
        InlineKeyboardButton("Non", callback_data="no"),
    ]

    spanish_options = [
        InlineKeyboardButton("Sí", callback_data="yes"),
        InlineKeyboardButton("No", callback_data="no"),
    ]

    if user_language == "fr":
        buttons = french_options
    elif user_language == "es":
        buttons = spanish_options
    else:
        buttons = english_options

    # Maximum options per row
    max_options_per_row = 1

    # Divide options into rows
    keyboard = []
    for i in range(0, len(buttons), max_options_per_row):
        keyboard.append(buttons[i : i + max_options_per_row])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def remove_all_data_keyboard(user_language: str) -> InlineKeyboardMarkup:

    english_options = [
        InlineKeyboardButton("Yes", callback_data="yes_delete"),
        InlineKeyboardButton("No", callback_data="no_delete"),
    ]

    french_options = [
        InlineKeyboardButton("Oui", callback_data="yes_delete"),
        InlineKeyboardButton("Non", callback_data="no_delete"),
    ]

    spanish_options = [
        InlineKeyboardButton("Sí", callback_data="yes_delete"),
        InlineKeyboardButton("No", callback_data="no_delete"),
    ]

    if user_language == "fr":
        buttons = french_options
    elif user_language == "es":
        buttons = spanish_options
    else:
        buttons = english_options

    # Maximum options per row
    max_options_per_row = 1

    # Divide options into rows
    keyboard = []
    for i in range(0, len(buttons), max_options_per_row):
        keyboard.append(buttons[i : i + max_options_per_row])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


########## Subscriptions menu ############


async def subscription_menu_from_menus(user_language: str) -> InlineKeyboardMarkup:

    english_options = [
        [
            InlineKeyboardButton(" 💳 Subscribe", callback_data="subscribe"),
        ],
        [
            InlineKeyboardButton("🔙", callback_data="settings_menu"),
            InlineKeyboardButton("🏠 Main menu", callback_data="main"),
        ],
    ]

    french_options = [
        [
            InlineKeyboardButton(" 💳 S'abonner", callback_data="subscribe"),
        ],
        [
            InlineKeyboardButton("🔙", callback_data="settings_menu"),
            InlineKeyboardButton("🏠 Menu principal", callback_data="main"),
        ],
    ]

    spanish_options = [
        [
            InlineKeyboardButton("💳 Suscribirse", callback_data="subscribe"),
        ],
        [
            InlineKeyboardButton("🔙", callback_data="settings_menu"),
            InlineKeyboardButton("🏠 Menú principal", callback_data="main"),
        ],
    ]

    if user_language == "fr":
        buttons = french_options
    elif user_language == "es":
        buttons = spanish_options
    else:
        buttons = english_options

    return InlineKeyboardMarkup(inline_keyboard=buttons)
