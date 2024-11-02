import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PreCheckoutQueryHandler,
    ShippingQueryHandler,
    filters,
)

from main import get_language_for_chat_id

load_dotenv()

PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN")

# NOTE : Le système d'abonnement est mis de côté.
# async def send_subscription_invoice(
#     update: Update, context: ContextTypes.DEFAULT_TYPE
# ) -> None:
#     """Sends an invoice without shipping-payment."""
#     query = update.callback_query
#     chat_id = query.message.chat_id
#     language = await get_language_for_chat_id(chat_id)

#     if language == "fr":
#         title = "Abonnement de 12 mois Premium."
#         description = "Accédez à un abonnement Premium de 12 mois. Cela vous permet d'obtenir jusqu'à 20 alertes. Il n'est pas renouvelé automatiquement chaque année."
#     elif language == "es":
#         title = "Suscripción de 12 meses de Premium."
#         description = "Obtenga acceso a una suscripción Premium durante 12 meses. Esto le permite recibir hasta 20 alertas. No se renueva automáticamente cada año."
#     else:  # Default to English
#         title = "Subscription for 12 months of Premium."
#         description = "Get access to a Premium subscription for 12 months. This allows you to get up to 20 alerts. It is not renewed automatically each year."

#     photo_url = "https://i.ibb.co/HBvGRZq/Untitled-Design.png"
#     photo_height = "1024"
#     photo_width = "1024"
#     # select a payload just for you to recognize it's the donation from your bot
#     payload = "Custom-Payload"
#     start_parameter = "start"
#     # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
#     currency = "EUR"
#     # price in dollars
#     price = 50
#     # price * 100 so as to include 2 decimal points
#     prices = [LabeledPrice("Test", price * 100)]

#     # optionally pass need_name=True, need_phone_number=True,
#     # need_email=True, need_shipping_address=True, is_flexible=True
#     await context.bot.send_invoice(
#         chat_id,
#         title,
#         description,
#         payload,
#         PAYMENT_PROVIDER_TOKEN,
#         currency,
#         prices,
#         start_parameter,
#         photo_url,
#         photo_height=photo_height,
#         photo_width=photo_width,
#     )


# NOTE : Le système de paiement est juste là pour ajouter des slots disponibles au nombre de wallets suivable
async def send_invoice(
    update: Update, context: ContextTypes.DEFAULT_TYPE, slot_count: int
) -> None:
    chat_id = update.message.chat_id
    language = await get_language_for_chat_id(chat_id)
    """Sends an invoice based on the selected slot count."""
    price_per_slot = 2  # Adjust price per slot as needed

    if language == "fr":
        title = "Achat de slots de portefeuilles à vie"
        description = (
            f"Achetez {slot_count} slot(s) de portefeuilles pour un accès à vie."
        )
    elif language == "es":
        title = "Compra de slots de billeteras vitalicios"
        description = (
            f"Compra {slot_count} slot(s) de billetera para acceso de por vida."
        )
    else:  # Default to English
        title = "Lifetime Wallets Slot Purchase"
        description = f"Purchase {slot_count} wallets slot(s) for lifetime access."

    photo_url = "https://i.ibb.co/HBvGRZq/Untitled-Design.png"
    photo_height = "1024"
    photo_width = "1024"
    # Generate the invoice details
    currency = "EUR"
    total_price = slot_count * price_per_slot * 100  # Multiplied by 100 for cents
    prices = [LabeledPrice(f"{slot_count} Slots", total_price)]

    # Send the invoice
    await context.bot.send_invoice(
        chat_id,
        title,
        description,
        "Custom-Payload",
        PAYMENT_PROVIDER_TOKEN,
        currency,
        prices,
        "start",
        photo_url,
        photo_height=photo_height,
        photo_width=photo_width,
    )
