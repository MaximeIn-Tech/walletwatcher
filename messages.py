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


#### HELP MESSAGES ###
async def help_menu(user_language: str):
    if user_language == "fr":
        return """Bienvenue dans la section d'aide du bot. 🤖

Pour faire fonctionner le bot, il vous suffit d'entrer une nouvelle alerte, de la configurer et c'est tout. 😊

Le seuil de déclenchement est le montant de tokens que vous souhaitez pour activer votre alerte.
Il fonctionne aussi bien pour les changements positifs que négatifs.
Par exemple, si votre point de déclenchement est 100 et que le portefeuille reçoit 90 tokens, aucune alerte ne sera envoyée.
Cependant, si le portefeuille retire 110 tokens, une alerte sera envoyée.

Vous pouvez consulter plus d'informations sur différents sujets en cliquant sur les boutons ci-dessous.

Créé avec soin par @TechSherpa. 👨‍💻
"""
    elif user_language == "es":
        return """Bienvenido/a a la sección de ayuda del bot. 🤖

Para hacer funcionar el bot, solo tienes que ingresar una nueva alerta, configurarla y listo. 😊

El punto de activación es la cantidad de tokens que deseas para activar tu alerta.
Funciona tanto para cambios positivos como negativos.
Por ejemplo, si tu punto de activación es 100 y la billetera recibe 90 tokens, no se enviará una alerta.
Sin embargo, si la billetera retira 110 tokens, se enviará una alerta.

Puedes ver más información sobre diferentes temas haciendo clic en los botones a continuación.

Creado con cuidado por @TechSherpa. 👨‍💻
"""
    else:
        return """Welcome to the help section of the bot. 🤖

To make the bot work, you just have to enter a new alert, set it up and that's it. 😊

The trigger point is the amount of tokens you want to trigger your alert.
It works for both positive and negative change.
For example, if your trigger point is 100 and the wallet receives 90 tokens, an alert won't be sent.
However, if the wallet withdraws 110 tokens, an alert will be sent.

You can view more information about different topics by clicking on the buttons below.

Created with care by @TechSherpa. 👨‍💻
"""


async def privacy_message(user_language: str):
    if user_language == "fr":
        return """Le bot prend soin de vos demandes et stocke vos données en toute sécurité dans une base de données.

Une grande importance est accordée à la protection de votre anonymat. Seul votre Chat_ID est conservé, garantissant ainsi que les messages vous parviennent précisément sans mélanger les données des autres utilisateurs.

De plus, le bot n'enregistre pas votre adresse IP, votre nom d'utilisateur ou d'autres détails qui pourraient vous identifier.
"""
    elif user_language == "es":
        return """El bot se encarga de tus solicitudes y almacena tus datos de forma segura en una base de datos.

Se otorga gran importancia a la protección de tu anonimato. Solo se conserva tu Chat_ID, garantizando que los mensajes te lleguen con precisión sin mezclar datos de otros usuarios.

Además, el bot no registra tu dirección IP, nombre de usuario u otros detalles que puedan identificarte.
"""
    else:
        return """The bot takes care of your requests and securely stores your data in a database.

Great importance is placed on protecting your anonymity. Only your Chat_ID is retained, ensuring that messages reach you accurately without mixing data from other users.

Furthermore, the bot does not record your IP address, username, or other details that could identify you.
"""


async def donation_message(user_language: str):
    if user_language == "fr":
        return """🎉 Si vous souhaitez soutenir mon travail et contribuer aux coûts du bot, vous pouvez faire un don aux adresses ci-dessous :

Pour les jetons TNT-20 :
-> 0xf383d4c2656bb5642efe0cf54c90b826b2991a5f
Pour les jetons ERC-20 :
-> 0xf383d4c2656bb5642efe0cf54c90b826b2991a5f
Pour les jetons BEP-20 :
-> 0xf383d4c2656bb5642efe0cf54c90b826b2991a5f

Pour tout autre don, veuillez m'envoyer un message direct @TechSherpa.

Merci beaucoup ! 🙏
TechSherpa 🦙
"""
    elif user_language == "es":
        return """🎉 Si deseas apoyar mi trabajo y ayudar a cubrir los costos del bot, puedes donar a las siguientes direcciones:

Para los tokens TNT-20:
-> 0xf383d4c2656bb5642efe0cf54c90b826b2991a5f
Para los tokens ERC-20:
-> 0xf383d4c2656bb5642efe0cf54c90b826b2991a5f
Para los tokens BEP-20:
-> 0xf383d4c2656bb5642efe0cf54c90b826b2991a5f

Para cualquier otra donación, por favor envíame un mensaje directo a @TechSherpa.

¡Muchas gracias! 🙏
TechSherpa 🦙
"""
    else:
        return """🎉 If you want to support my work and support the cost of the bot, you can donate on these addresses below:

For TNT-20 tokens:
-> 0xf383d4c2656bb5642efe0cf54c90b826b2991a5f
For ERC-20 tokens:
-> 0xf383d4c2656bb5642efe0cf54c90b826b2991a5f
For BEP-20 tokens:
-> 0xf383d4c2656bb5642efe0cf54c90b826b2991a5f

For any other donations, please send me a direct message @TechSherpa.

Thanks a lot! 🙏
TechSherpa 🦙
"""


async def data_collection_message(user_language: str):
    if user_language == "fr":
        return """🌐 Les données sont collectées sur différents sites web via des API.

Le bot utilise :
- Thetascan.io pour la blockchain Theta.
- Explorer.thetatoken.org pour les Stakes Theta (vérifiées toutes les heures).
- Etherscan.io pour la blockchain Ethereum.
- Bscscan.io pour la blockchain BSC.

Les soldes sont vérifiés toutes les 10 minutes.
Pour les stakes Theta, les mises sont vérifiées toutes les heures.
"""
    elif user_language == "es":
        return """🌐 Los datos se recopilan en diferentes sitios web a través de APIs.

El bot utiliza:
- Thetascan.io para la blockchain de Theta.
- Explorer.thetatoken.org para las apuestas en Theta (verificadas cada hora).
- Etherscan.io para la blockchain de Ethereum.
- Bscscan.io para la blockchain de BSC.

Los saldos se verifican cada 10 minutos.
Para los apostadores Theta, las apuestas se verifican cada hora.
"""
    else:
        return """🌐 Data is collected on different websites throught APIs.

The bot uses:
- Thetascan.io for Theta Blockchain.
- Explorer.thetatoken.org for Theta Stakes (checked every hour).
- Etherscan.io for Ethereum Blockchain.
- Bscscan.io for BSC Blockchain.

Balances are checked every 10 minutes.
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
        return f"Vous avez atteint votre limite d'alerte.\nPour en ajouter plus, supprimez-en une existante ou abonnez-vous."
    elif user_language == "es":
        return f"Ha alcanzado su límite de alerta.\nPara añadir más, elimina una existente o suscríbete."
    else:
        return f"You've reached your alert limit.\nTo add more, delete an existing one or subscribe."


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


async def subscription_explanation(user_language, subscription, end_date):

    if user_language == "fr":
        if subscription and subscription != "Free" and end_date:
            return f"""Bienvenue dans le menu d'abonnement.

Avec un abonnement gratuit, vous pouvez bénéficier jusqu'à 5 alertes.

Si vous en voulez plus, vous pouvez vous abonner à l'abonnement Premium, qui vous donnera accès à 20 alertes.

Il coûte 50€/an et n'est pas renouvelé automatiquement. Après 1 an, vous serez désabonné si vous ne renouvelez pas.
Vous pouvez payer plusieurs fois et cela ajoutera un an pour chaque paiement réussi.

Si vous souhaitez vous abonner, cliquez sur le bouton ci-dessous.

Votre abonnement actuel est "{subscription}" et se termine le {end_date.strftime('%d/%m/%Y à %H:%M:%S')}.
        """
        else:
            return f"""Bienvenue dans le menu d'abonnement.

Avec un abonnement gratuit, vous pouvez bénéficier jusqu'à 5 alertes.

Si vous en voulez plus, vous pouvez vous abonner à l'abonnement Premium, qui vous donnera accès à 20 alertes.

Il coûte 50€/an et n'est pas renouvelé automatiquement. Après 1 an, vous serez désabonné si vous ne renouvelez pas.
Vous pouvez payer plusieurs fois et cela ajoutera un an pour chaque paiement réussi.

Si vous souhaitez vous abonner, cliquez sur le bouton ci-dessous.
        """
    elif user_language == "es":
        if subscription and subscription != "Free" and end_date:
            return f"""Bienvenido al menú de suscripción.


Con una suscripción gratuita, puedes tener hasta 5 alertas.

Si deseas más, puedes suscribirte a la suscripción Premium, que te concederá 20 alertas.

Cuesta 50€/año y no se renueva automáticamente. Después de 1 año, serás dado de baja si no renuevas.
Puedes pagar varias veces y se añadirá un año por cada pago exitoso.

Si deseas suscribirte, haz clic en el botón a continuación.

Tu suscripción actual es "{subscription}" y termina el {end_date.strftime('%d/%m/%Y a las %H:%M:%S')}.
"""
        else:
            return f"""Bienvenido al menú de suscripción.

Con una suscripción gratuita, puedes tener hasta 5 alertas.

Si deseas más, puedes suscribirte a la suscripción Premium, que te concederá 20 alertas.

Cuesta 50€/año y no se renueva automáticamente. Después de 1 año, serás dado de baja si no renuevas.
Puedes pagar varias veces y se añadirá un año por cada pago exitoso.

Si deseas suscribirte, haz clic en el botón a continuación.
"""
    else:
        if subscription and subscription != "Free" and end_date:
            return f"""Welcome to the subscription menu.

With a Free subscription, you can have up to 5 alerts.

If you want more, you can subscribe to the Premium subscription, which will grant you 20 alerts.

It costs 50€/year and is not an automatic renew. After 1 year, you'll be opted-out if you don't repay.
You can pay multiple times and it will ad one year for every succesful payment.

If you want to subscribe, click the button below.

Your current subscription is "{subscription}" and ends {end_date.strftime('%d/%m/%Y at %H:%M:%S')}
"""
        else:
            return f"""Welcome to the subscription menu.

With a Free subscription, you can have up to 5 alerts.

If you want more, you can subscribe to the Premium subscription, which will grant you 20 alerts.

It costs 50€/year and is not an automatic renew. After 1 year, you'll be opted-out if you don't repay.
You can pay multiple times and it will ad one year for every succesful payment.

If you want to subscribe, click the button below.
"""


async def subscription_succesfull_first_time(user_language, new_end_date):

    if user_language == "fr":
        return f"Merci pour votre paiement ! Vous avez maintenant accès à l'abonnement Premium jusqu'au {new_end_date.strftime('%Y-%m-%d')}."
    elif user_language == "es":
        return f"¡Gracias por tu pago! Ahora tienes acceso a la suscripción Premium hasta el {new_end_date.strftime('%Y-%m-%d')}."
    else:
        return f"Thank you for your payment! You now have access to the Premium subscription until {new_end_date.strftime('%Y-%m-%d')}."


async def subscription_succesfull_more_time(user_language, new_end_date):

    if user_language == "fr":
        return f"Merci d'avoir renouvelé votre abonnement ! Votre accès Premium a été prolongé jusqu'au {new_end_date.strftime('%Y-%m-%d')}."
    elif user_language == "es":
        return f"¡Gracias por renovar tu suscripción! Tu acceso Premium ha sido extendido hasta el {new_end_date.strftime('%Y-%m-%d')}."
    else:
        return f"Thank you for renewing your subscription! Your Premium access has been extended until {new_end_date.strftime('%Y-%m-%d')}."


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
            symbol = symbol.upper()
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
            symbol = symbol.upper()
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
            symbol = symbol.upper()
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
