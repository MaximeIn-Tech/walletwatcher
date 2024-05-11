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
        return "Veuillez entrer le seuil de déclenchement <i>(choisissez 0 si vous voulez voir chaque mise à jour)</i> :"
    elif user_language == "es":
        return "Por favor, ingresa el punto de activación <i>(elige 0 si deseas ver cada actualización)</i>:"
    else:
        return "Please enter the trigger point <i>(choose 0 if you want to see every update)</i>:"


async def trigger_point_saved(user_language: str, trigger_point):
    if user_language == "fr":
        return f"Seuil de déclenchement {trigger_point} enregistré."
    elif user_language == "es":
        return f"Punto de activación {trigger_point} guardado."
    else:
        return f"Trigger point {trigger_point} saved."


async def trigger_point_error(user_language: str):
    if user_language == "fr":
        return "Veuillez entrer un seuil de déclenchement valide."
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
            "Your followed wallets are (click on one to see what contract is followed):"
        )


async def no_wallets_found(user_language: str):
    if user_language == "fr":
        return "Aucun portefeuille n'a été trouvé."
    elif user_language == "es":
        return "No se encontraron carteras."
    else:
        return "No wallets have been found."


async def no_setups_found(user_language: str):
    if user_language == "fr":
        return "Aucune alerte n'a été trouvé pour ce portefeuille."
    elif user_language == "es":
        return "No se han encontrado alertas para esta cartera."
    else:
        return "No alerts have been found for this wallet."


async def setups_found(user_language, formatted_setups, wallet_address):
    if user_language == "fr":
        return f"Alertes pour le portefeuille sélectionné :\n{wallet_address}\n\n{formatted_setups}"
    elif user_language == "es":
        return f"Alertas para el monedero seleccionado :\n{wallet_address}\n\n{formatted_setups}"
    else:
        return f"Alerts for selected wallet:\n{wallet_address}\n\n{formatted_setups}"


async def alert_text(user_language):
    if user_language == "fr":
        return f"Alerte"
    elif user_language == "es":
        return f"Alerta"
    else:
        return f"Alert"


async def use_buttons(user_language):
    if user_language == "fr":
        return f"Veuillez utiliser les boutons du menu."
    elif user_language == "es":
        return f"Por favor, utiliza los botones del menú."
    else:
        return f"Please use the menu's buttons."


async def too_many_setups(user_language):
    if user_language == "fr":
        return f"Vous avez atteint la limite de 5 alertes gratuites. Pour en ajouter plus, supprimez-en une existante ou abonnez-vous."
    elif user_language == "es":
        return f"Has alcanzado el límite de 5 alertas gratuitas. Para añadir más, elimina una existente o suscríbete."
    else:
        return f"You've reached the limit of 5 free alerts. To add more, delete an existing one or subscribe."


##### DELETE SECTION


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


async def setup_deletion_success(user_language):
    if user_language == "fr":
        return f"L'alerte sélectionnée a bien été supprimée. Pour en supprimer une nouvelle, cliquez sur Back."
    elif user_language == "es":
        return f"La alerta seleccionada ha sido eliminada correctamente. Para eliminar otra, haga clic en Back."
    else:
        return f"The selected alert has been successfully deleted. To delete another one, click on Back."


async def setup_to_delete_1(user_language):
    if user_language == "fr":
        return f"Voici vos alertes pour ce portefeuille :"
    elif user_language == "es":
        return f"Aquí están tus alertas para este monedero:"
    else:
        return f"Here are your alerts for this wallet:"


async def setup_to_delete_2(user_language):
    if user_language == "fr":
        return f"Veuillez sélectionner celle que vous souhaitez supprimer."
    elif user_language == "es":
        return f"Por favor selecciona la que deseas eliminar."
    else:
        return f"Please select one you want to delete."


############# Subscriptions Menus ######################


async def subscription_explanation(user_language):
    if user_language == "fr":
        return f"Pour le moment, vous pouvez avoir jusqu'à 10 alertes dans la version gratuite. D'autres abonnements seront disponibles bientôt..."
    elif user_language == "es":
        return f"Por ahora, puedes tener hasta 10 alertas en la versión gratuita. ¡Más suscripciones próximamente..."
    else:
        return f"You can have up to 10 alerts for now while on the free version. More subscriptions to come..."


match_table = {
    "eenp": "Edge Node",
    "gcp": "Guardian Node",
    "vcp": "Validator Node",
}

match_table_token = {
    "eenp": "TFUEL",
    "gcp": "THETA",
    "vcp": "THETA.",
}


async def tracked_wallet_setup_message(
    wallet_name,
    blockchain,
    wallet_address,
    symbol,
    contract_address,
    trigger_point,
    balance,
    stake,
    language,
):
    if language == "fr":
        message = f"Configuration du portefeuille suivi :\n\n"
        message += f"Nom du portefeuille : {wallet_name}\n"
        message += f"Blockchain : {blockchain}\n"
        message += f"Adresse du portefeuille : {wallet_address}\n"
        if symbol == "Stake Watch":
            if stake["sourceRecords"]:
                message += f"Stake watch:\n"
                for record in stake["sourceRecords"]:
                    record_type = record["type"]
                    amount = int(record["amount"]) * (10**-18)
                    # Format the amount with spaces every three digits
                    formatted_amount = "{:,.2f}".format(amount).replace(
                        ",", " "
                    )  # Replace commas with spaces
                    if record_type in match_table:
                        message_to_add = match_table[record_type]
                        token = match_table_token[record_type]
                        message += f"{message_to_add} avec {formatted_amount} {token} stakés.\n"
            else:
                message += "Rien n'est staké depuis ce portefeuille.\n"
        elif symbol is not None:
            symbol = symbol.capitalize()
            message += f"Symbole du jeton : {symbol}\n"
        if contract_address is not None:
            message += f"Adresse du contrat : {contract_address}\n"
        if trigger_point is not None:
            message += f"Seuil de déclenchement : {trigger_point}\n"
        if balance is not None:
            message += f"Votre solde actuel est : {balance} {symbol}"
    elif language == "es":
        message = f"Configuración del monedero rastreado:\n\n"
        message += f"Nombre del monedero: {wallet_name}\n"
        message += f"Blockchain: {blockchain}\n"
        message += f"Dirección del monedero: {wallet_address}\n"
        if symbol == "Stake Watch":
            if stake["sourceRecords"]:
                message += f"Stake watch:\n"
                for record in stake["sourceRecords"]:
                    record_type = record["type"]
                    amount = int(record["amount"]) * (10**-18)
                    # Format the amount with spaces every three digits
                    formatted_amount = "{:,.2f}".format(amount).replace(
                        ",", " "
                    )  # Replace commas with spaces
                    if record_type in match_table:
                        message_to_add = match_table[record_type]
                        token = match_table_token[record_type]
                        message += f"{message_to_add} con {formatted_amount} {token} apostadas.\n"
            else:
                message += "No se almacena nada en esta cartera.\n"
        elif symbol is not None:
            symbol = symbol.capitalize()
            message += f"Símbolo del token: {symbol}\n"
        if contract_address is not None:
            message += f"Dirección del contrato: {contract_address}\n"
        if trigger_point is not None:
            message += f"Punto de activación: {trigger_point}\n"
        if balance is not None:
            message += f"Tu saldo actual es: {balance} {symbol}"
    else:  # English
        message = f"Tracked wallet setup:\n\n"
        message += f"Wallet Name: {wallet_name}\n"
        message += f"Blockchain: {blockchain}\n"
        message += f"Wallet Address: {wallet_address}\n"
        if symbol == "Stake Watch":
            if stake["sourceRecords"]:
                message += f"Stake watch:\n"
                for record in stake["sourceRecords"]:
                    record_type = record["type"]
                    amount = int(record["amount"]) * (10**-18)
                    # Format the amount with spaces every three digits
                    formatted_amount = "{:,.2f}".format(amount).replace(
                        ",", " "
                    )  # Replace commas with spaces
                    if record_type in match_table:
                        message_to_add = match_table[record_type]
                        token = match_table_token[record_type]
                        message += f"{message_to_add} with {formatted_amount} {token} staked.\n"
            else:
                message += "Nothing is staked from this wallet.\n"
        elif symbol is not None:
            symbol = symbol.capitalize()
            message += f"Token Symbol: {symbol}\n"
        if contract_address is not None:
            message += f"Contract Address: {contract_address}\n"
        if trigger_point is not None:
            message += f"Trigger Point: {trigger_point}\n"
        if balance is not None:
            message += f"Your current balance is : {balance} {symbol}"

    return message


def generate_formatted_setups(setups, alert, user_language):
    formatted_setups = ""
    for n, setup in enumerate(setups.data, start=1):

        if user_language == "fr":
            formatted_setups += f"{alert} {n}:"
            formatted_setups += f"\nBlockchain: {setup['blockchain']}"
            if setup["token_symbol"] == "Stake Watch":
                stake = setup["stake_data"]
                formatted_setups += f"\nStake Watch!\n"
                if stake["sourceRecords"]:
                    formatted_setups += f"Vos stakes sont:\n"
                    for record in stake["sourceRecords"]:
                        record_type = record["type"]
                        amount = int(record["amount"]) * (10**-18)
                        # Format the amount with spaces every three digits
                        formatted_amount = "{:,.2f}".format(amount).replace(
                            ",", " "
                        )  # Replace commas with spaces
                        if record_type in match_table:
                            message_to_add = match_table[record_type]
                            token = match_table_token[record_type]
                            formatted_setups += f"{message_to_add} avec {formatted_amount} {token} stakés.\n"
                else:
                    formatted_setups += "Rien n'est staké pour le moment.\n"
            elif setup["token_symbol"] is not None:
                formatted_setups += f"\nToken: {setup['token_symbol']}"
            if setup["contract_address"] is not None:
                formatted_setups += f"\nContract Address: {setup['contract_address']}"
            if setup["trigger_point"] is not None:
                formatted_setups += (
                    f"\nSeuil de déclenchement: {setup['trigger_point']}"
                )
            if setup["balance"] is not None:
                formatted_setups += (
                    f"\nSolde actuel: {setup['balance']} {setup['token_symbol']}"
                )
            formatted_setups += "\n\n"
        elif user_language == "es":
            formatted_setups += f"{alert} {n}:"
            formatted_setups += f"\nBlockchain: {setup['blockchain']}"
            if setup["token_symbol"] == "Stake Watch":
                stake = setup["stake_data"]
                formatted_setups += f"\nStake Watch!\n"
                if stake["sourceRecords"]:
                    formatted_setups += f"Vos stakes sont:\n"
                    for record in stake["sourceRecords"]:
                        record_type = record["type"]
                        amount = int(record["amount"]) * (10**-18)
                        # Format the amount with spaces every three digits
                        formatted_amount = "{:,.2f}".format(amount).replace(
                            ",", " "
                        )  # Replace commas with spaces
                        if record_type in match_table:
                            message_to_add = match_table[record_type]
                            token = match_table_token[record_type]
                            formatted_setups += f"{message_to_add} con {formatted_amount} {token} apostadas.\n"
                else:
                    formatted_setups += "Rien n'est staké pour le moment.\n"
            elif setup["token_symbol"] is not None:
                formatted_setups += f"T\noken: {setup['token_symbol']}"
            if setup["contract_address"] is not None:
                formatted_setups += (
                    f"\nDirección del Contrato: {setup['contract_address']}"
                )
            if setup["trigger_point"] is not None:
                formatted_setups += f"\nPunto de Activación: {setup['trigger_point']}"
            if setup["balance"] is not None:
                formatted_setups += (
                    f"\nSaldo: {setup['balance']} {setup['token_symbol']}"
                )
            formatted_setups += "\n\n"
        # Add more language conditions as needed
        else:
            # Default to English if language not specified or recognized
            formatted_setups += f"{alert} {n}:"
            formatted_setups += f"\nBlockchain: {setup['blockchain']}"
            if setup["token_symbol"] == "Stake Watch":
                stake = setup["stake_data"]
                formatted_setups += f"\nStake Watch!\n"
                if stake["sourceRecords"]:
                    formatted_setups += f"Your stakes are:\n"
                    for record in stake["sourceRecords"]:
                        record_type = record["type"]
                        amount = int(record["amount"]) * (10**-18)
                        # Format the amount with spaces every three digits
                        formatted_amount = "{:,.2f}".format(amount).replace(
                            ",", " "
                        )  # Replace commas with spaces
                        if record_type in match_table:
                            message_to_add = match_table[record_type]
                            token = match_table_token[record_type]
                            formatted_setups += f"{message_to_add} with {formatted_amount} {token} staked.\n"
                else:
                    formatted_setups += "Nothing is staked from this wallet.\n"
            elif setup["token_symbol"] is not None:
                formatted_setups += f"\nToken: {setup['token_symbol']}"
            if setup["contract_address"] is not None:
                formatted_setups += f"\nContract Address: {setup['contract_address']}"
            if setup["trigger_point"] is not None:
                formatted_setups += f"\nTrigger Point: {setup['trigger_point']}"
            if setup["balance"] is not None:
                formatted_setups += (
                    f"\nCurrent balance: {setup['balance']} {setup['token_symbol']}"
                )
            formatted_setups += "\n\n"
    return formatted_setups
