######## MENU MESSAGES ###########
async def main_menu_message(username, user_language):
    if user_language == "fr":
        return f"""🚀 Bienvenue sur Crypto Wallet Monitor {username}, conçu avec soin par @TechSherpa !

Prêt à rester informé en temps réel dès que des transactions se produisent dans vos portefeuilles de cryptomonnaie ? Commençons !

Avec ce bot intuitif, vous pouvez choisir manuellement vos portefeuilles sur différentes blockchains, définir vos préférences et rester informé des mises à jour précisément quand vous le souhaitez.

Explorez notre ensemble de commandes :
"""
    else:
        # Default message for unsupported languages or English
        return f"""🚀 Welcome to Crypto Wallet Monitor {username}, crafted with care by @TechSherpa!

Ready to stay in the loop with real-time alerts whenever transactions occur in your crypto wallets? Let's get started!

With this intuitive bot, you can handpick wallets from various blockchains, set your preferences, and stay in the loop with updates precisely when you desire.

Explore our suite of commands:
"""


async def help_message(user_language: str):
    if user_language == "fr":
        return """Le bot prend soin de vos demandes et stocke vos données en toute sécurité dans une base de données.

Nous accordons une grande importance à la protection de votre anonymat. Seul votre Chat_ID est conservé, ce qui garantit que les messages vous parviennent précisément sans mélanger les données des autres utilisateurs.

De plus, le bot n'enregistre pas votre adresse IP, votre nom d'utilisateur ou d'autres détails qui pourraient vous identifier.
"""
    else:
        # Default message for unsupported languages or English
        return """The bot attentively processes your inquiries and securely stores your data within a database. 
    
Maintaining user anonymity is paramount; hence, only your Chat_ID is retained, ensuring precise message delivery without intertwining data from various users. 
    
Additionally, the bot refrains from logging your IP, username, or any other details that could potentially identify you as a user.
"""


###### OPTIONS MESSAGES #####
async def settings_message(user_language: str):
    if user_language == "fr":
        return "Choisissez l'option que vous voulez modifier:"
    else:
        return "Please choose a setting you want to adjust:"


async def language_selection_message(user_language: str):
    if user_language == "fr":
        return "Choisissez une langue:"
    else:
        return "Please choose a language you prefer:"


####### ADD WALLET MESSAGES


async def blockchain_choice_message(user_language: str):
    if user_language == "fr":
        return "Choisissez une blockchain:"
    else:
        return "Please select a blockchain:"


async def address_choice_message(user_language: str, selected_blockchain: str):
    if user_language == "fr":
        return f"Veuillez entrer une adresse de portefeuille {selected_blockchain} :"
    else:
        return f"Please enter any {selected_blockchain} wallet address:"


async def address_confirmation_message(user_language: str, wallet_address: str):
    if user_language == "fr":
        return f"Votre adresse de portefeuille est {wallet_address}.\nSouhaitez-vous donner un nom à cette adresse ?"
    else:
        return (
            f"Your wallet address is {wallet_address}.\nWould you like to name that address?",
        )


async def wallet_address_error(user_language: str):
    if user_language == "fr":
        return "Veuillez saisir une adresse de portefeuille valide"
    else:
        return "Please enter a valid wallet address."


async def naming_wallet(user_language: str):
    if user_language == "fr":
        return "Veuillez saisir le nom du portefeuille :"
    else:
        return "Please enter the name of the wallet:"


async def token_symbol_choice(user_language: str):
    if user_language == "fr":
        return "Veuillez choisir un token :"
    else:
        return "Please select a token symbol:"


async def contract_address_selection(user_language: str):
    if user_language == "fr":
        return "Veuillez saisir l'adresse du contrat :"
    else:
        return "Please enter the contract address:"


async def custom_contract_address(user_language: str, contract_address: str):
    if user_language == "fr":
        return f"Adresse du contrat {contract_address} enregistrée."
    else:
        return f"Contract address {contract_address} saved."


async def contract_address_error(user_language: str):
    if user_language == "fr":
        return "Veuillez saisir une adresse de contrat valide :"
    else:
        return "Please enter a valid contract address."


async def trigger_point_selection(user_language: str):
    if user_language == "fr":
        return "Veuillez entrer le point de déclenchement <i>(choisissez 0 si vous voulez voir chaque mise à jour)</i> :"
    else:
        return "Please enter the trigger point <i>(choose 0 if you want to see every update)</i>:"


async def trigger_point_saved(user_language: str, trigger_point):
    if user_language == "fr":
        return f"Point de déclenchement {trigger_point} enregistré."
    else:
        return f"Trigger point {trigger_point} saved."


async def trigger_point_error(user_language: str):
    if user_language == "fr":
        return "Veuillez entrer un point de déclenchement valide."
    else:
        return "Please enter a valid trigger point."


async def stake_message(user_language: str):
    if user_language == "fr":
        return "L'état de vos stakes sont surveillés. Vous recevrez un message si ils sont en cours d'unstaking."
    else:
        return "Stakes on this wallet are being watched. You'll be notified if a stake is withdrawn."


async def tracked_wallet_setup_message(
    wallet_name,
    blockchain,
    wallet_address,
    symbol,
    contract_address,
    trigger_point,
    language,
):
    if language == "fr":
        message = f"Configuration du portefeuille suivi :\n\n"
        message += f"Nom du portefeuille : {wallet_name}\n"
        message += f"Blockchain : {blockchain}\n"
        message += f"Adresse du portefeuille : {wallet_address}\n"
        message += f"Symbole du jeton : {symbol}\n"
        if contract_address is not None:
            message += f"Adresse du contrat : {contract_address}\n"
        message += f"Point de déclenchement : {trigger_point}"
    else:  # English
        message = f"Tracked wallet setup:\n\n"
        message += f"Wallet Name: {wallet_name}\n"
        message += f"Blockchain: {blockchain}\n"
        message += f"Wallet Address: {wallet_address}\n"
        message += f"Token Symbol: {symbol}\n"
        if contract_address is not None:
            message += f"Contract Address: {contract_address}\n"
        message += f"Trigger Point: {trigger_point}"

    return message
