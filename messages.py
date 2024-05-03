######## MENU MESSAGES ###########
async def main_menu_message(username, user_language):
    if user_language == "fr":
        return f"""🚀 Bienvenue sur Crypto Wallet Monitor {username}, votre allié pour surveiller vos cryptos de près !

Ce bot vous alerte dès que le solde de vos portefeuilles change. Restez connecté à vos investissements et ne ratez aucune variation importante !

Prêt à être notifié à chaque mouvement ? Ajoutez vos portefeuilles et gardez le contrôle total ! 🚨
"""
    elif user_language == "es":
        return f"""🚀 ¡Bienvenido a Crypto Wallet Monitor {username}, tu aliado para vigilar de cerca tus criptomonedas!

Este bot te alerta cada vez que el saldo de tu carteras cambia. ¡Mantente conectado a tus inversiones y no te pierdas ninguna fluctuación importante!

¿Listo para recibir notificaciones con cada movimiento? ¡Agrega tus carteras y mantén el control total! 🚨
        """
    else:
        # Default message for unsupported languages or English
        return f"""🚀 Welcome to Crypto Wallet Monitor {username}, your ally for keeping a close eye on your cryptos!

This bot alerts you whenever your wallets balance changes. Stay connected to your investments and never miss an important fluctuation!

Ready to be notified with every move? Add your wallets and stay in complete control! 🚨
"""


async def help_message(user_language: str):
    if user_language == "fr":
        return """Le bot prend soin de vos demandes et stocke vos données en toute sécurité dans une base de données.

Une grande importance est accordée à la protection de votre anonymat. Seul votre Chat_ID est conservé, garantissant ainsi que les messages vous parviennent précisément sans mélanger les données des autres utilisateurs.

De plus, le bot n'enregistre pas votre adresse IP, votre nom d'utilisateur ou d'autres détails qui pourraient vous identifier.

Créé par @TechSherpa.
"""
    elif user_language == "es":
        return """El bot se encarga de tus solicitudes y almacena tus datos de forma segura en una base de datos.

Se otorga gran importancia a la protección de tu anonimato. Solo se conserva tu Chat_ID, garantizando que los mensajes te lleguen con precisión sin mezclar datos de otros usuarios.

Además, el bot no registra tu dirección IP, nombre de usuario u otros detalles que puedan identificarte.

Creado por @TechSherpa.
"""
    else:
        return """The bot takes care of your requests and securely stores your data in a database.

Great importance is placed on protecting your anonymity. Only your Chat_ID is retained, ensuring that messages reach you accurately without mixing data from other users.

Furthermore, the bot does not record your IP address, username, or other details that could identify you.

Created by @TechSherpa.
"""


###### OPTIONS MESSAGES #####
async def settings_message(user_language: str):
    if user_language == "fr":
        return "Choisissez l'option que vous voulez modifier:"
    elif user_language == "es":
        return "Por favor, elige la configuración que deseas ajustar:"
    else:
        return "Please choose a setting you want to adjust:"


async def language_selection_message(user_language: str):
    if user_language == "fr":
        return "Choisissez une langue:"
    elif user_language == "es":
        return "Por favor, elige el idioma que prefieres:"
    else:
        return "Please choose a language you prefer:"


####### ADD WALLET MESSAGES


async def blockchain_choice_message(user_language: str):
    if user_language == "fr":
        return "Choisissez une blockchain:"
    elif user_language == "es":
        return "Por favor, selecciona una blockchain:"
    else:
        return "Please select a blockchain:"


async def address_choice_message(user_language: str, selected_blockchain: str):
    if user_language == "fr":
        return f"Veuillez entrer une adresse de portefeuille {selected_blockchain} :"
    elif user_language == "es":
        return f"Por favor, ingresa una dirección de monedero {selected_blockchain}:"
    else:
        return f"Please enter any {selected_blockchain} wallet address:"


async def address_confirmation_message(user_language: str, wallet_address: str):
    if user_language == "fr":
        return f"Votre adresse de portefeuille est {wallet_address}.\nSouhaitez-vous donner un nom à cette adresse ?"
    elif user_language == "es":
        return f"Tu dirección de monedero es {wallet_address}.\n¿Te gustaría darle un nombre a esta dirección?"
    else:
        return f"Your wallet address is {wallet_address}.\n Would you like to name that address?"


async def wallet_address_error(user_language: str):
    if user_language == "fr":
        return "Veuillez saisir une adresse de portefeuille valide"
    elif user_language == "es":
        return "Por favor, ingresa una dirección de monedero válida."
    else:
        return "Please enter a valid wallet address."


async def naming_wallet(user_language: str):
    if user_language == "fr":
        return "Veuillez saisir le nom du portefeuille :"
    elif user_language == "es":
        return "Por favor, ingresa el nombre del monedero:"
    else:
        return "Please enter the name of the wallet:"


async def token_symbol_choice(user_language: str):
    if user_language == "fr":
        return "Veuillez choisir un token :"
    elif user_language == "es":
        return "Por favor, selecciona un símbolo de token:"
    else:
        return "Please select a token symbol:"


async def contract_address_selection(user_language: str):
    if user_language == "fr":
        return "Veuillez saisir l'adresse du contrat :"
    elif user_language == "es":
        return "Por favor, ingresa la dirección del contrato:"
    else:
        return "Please enter the contract address:"


async def custom_contract_address(user_language: str, contract_address: str):
    if user_language == "fr":
        return f"Adresse du contrat {contract_address} enregistrée."
    elif user_language == "es":
        return f"Dirección del contrato {contract_address} guardada."
    else:
        return f"Contract address {contract_address} saved."


async def contract_address_error(user_language: str):
    if user_language == "fr":
        return "Veuillez saisir une adresse de contrat valide :"
    elif user_language == "es":
        return "Por favor, ingresa una dirección de contrato válida."
    else:
        return "Please enter a valid contract address."


async def trigger_point_selection(user_language: str):
    if user_language == "fr":
        return "Veuillez entrer le point de déclenchement <i>(choisissez 0 si vous voulez voir chaque mise à jour)</i> :"
    elif user_language == "es":
        return "Por favor, ingresa el punto de activación <i>(elige 0 si deseas ver cada actualización)</i>:"
    else:
        return "Please enter the trigger point <i>(choose 0 if you want to see every update)</i>:"


async def trigger_point_saved(user_language: str, trigger_point):
    if user_language == "fr":
        return f"Point de déclenchement {trigger_point} enregistré."
    elif user_language == "es":
        return f"Punto de activación {trigger_point} guardado."
    else:
        return f"Trigger point {trigger_point} saved."


async def trigger_point_error(user_language: str):
    if user_language == "fr":
        return "Veuillez entrer un point de déclenchement valide."
    elif user_language == "es":
        return "Por favor, ingresa un punto de activación válido."
    else:
        return "Please enter a valid trigger point."


async def stake_message(user_language: str):
    if user_language == "fr":
        return "L'état de vos stakes sont surveillés. Vous recevrez un message si ils sont en cours d'unstaking."
    elif user_language == "es":
        return "Los stakes en este monedero están siendo vigilados. Serás notificado si se retira algún stake."
    else:
        return "Stakes on this wallet are being watched. You'll be notified if a stake is withdrawn."


async def wallets_found_track(user_language: str):
    if user_language == "fr":
        return "Sélectionnez un portefeuille:"
    elif user_language == "es":
        return "Tus carteras seguidas son (haz clic en una para ver qué contrato está seguido) :"
    else:
        return "Select a wallet:"


async def wallets_found(user_language: str):
    if user_language == "fr":
        return "Vos portefeuilles suivis sont (cliquez sur l'un d'eux pour voir quels contrats sont suivis) :"
    elif user_language == "es":
        return "Tus carteras seguidas son (haz clic en una para ver qué contrato está seguido) :"
    else:
        return (
            "Your wallet followed are (click on one to see what contract is followed):"
        )


async def no_wallets_found(user_language: str):
    if user_language == "fr":
        return "Aucun portefeuille n'a été trouvé."
    elif user_language == "es":
        return "No se encontraron carteras."
    else:
        return "No wallets have been found."


async def no_contracts_found(user_language: str):
    if user_language == "fr":
        return "Aucun contrat n'a été trouvé pour ce portefeuille."
    elif user_language == "es":
        return "No se encontraron contratos para este monedero."
    else:
        return "No contracts have been found for this wallet."


async def contracts_found(user_language, formatted_contracts):
    if user_language == "fr":
        return f"Contrats pour le portefeuille sélectionné :\n{formatted_contracts}"
    elif user_language == "es":
        return f"Contratos para el monedero seleccionado :\n{formatted_contracts}"
    else:
        return f"Contracts for selected wallet:\n{formatted_contracts}"


async def remove_all_data(user_language):
    if user_language == "fr":
        return f"Voulez-vous vraiment supprimer toutes vos données ?"
    elif user_language == "es":
        return f"¿Estás seguro/a de que quieres eliminar todos tus datos?"
    else:
        return f"Are you sure you want to delete all your data?"


async def all_data_removed(user_language):
    if user_language == "fr":
        return f"Toutes vos données ont été supprimées."
    elif user_language == "es":
        return f"Todos sus datos han sido borrados."
    else:
        return f"All of your data has been deleted."


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
    elif language == "es":
        message = f"Configuración del monedero rastreado:\n\n"
        message += f"Nombre del monedero: {wallet_name}\n"
        message += f"Blockchain: {blockchain}\n"
        message += f"Dirección del monedero: {wallet_address}\n"
        message += f"Símbolo del token: {symbol}\n"
        if contract_address is not None:
            message += f"Dirección del contrato: {contract_address}\n"
        message += f"Punto de activación: {trigger_point}"
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
