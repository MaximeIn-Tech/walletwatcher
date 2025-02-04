import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes
from tqdm import tqdm

from database import *

load_dotenv()

ADMIN_ID = os.getenv("ADMIN_ID")  # Replace with your actual admin ID
TEST_ID_1 = os.getenv("TEST_ID_1")
TEST_ID_2 = os.getenv("TEST_ID_2")


async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message to all registered users."""
    if str(update.effective_user.id) != ADMIN_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    # Get the entire message after the command
    message = update.message.text[len("/broadcast ") :]  # Adjust based on your command
    if not message:
        await update.message.reply_text("Please provide a message to send.")
        return

    supabase = connect_to_database()

    # Retrieve all registered user chat IDs
    users = supabase.table("Users").select("chat_id").execute()

    if users.data:
        # Create a progress bar for sending messages
        for user in tqdm(users.data, desc="Sending messages", unit="user"):
            chat_id = user["chat_id"]
            try:
                await context.bot.send_message(chat_id, message, parse_mode="Markdown")
            except Exception as e:
                print(f"Could not send message to {chat_id}: {e}")

        await update.message.reply_text("Message sent to all users.")
    else:
        await update.message.reply_text("No registered users found.")


async def broadcast_message_test(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Send a message to all registered users while maintaining formatting."""
    print(f"Broadcast command received from {update.effective_user.id}")

    if str(update.effective_user.id) != ADMIN_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    # Extract the message from the command
    message = update.message.text[len("/broadcast ") :].strip()
    if not message and not update.message.photo:
        await update.message.reply_text(
            "Please provide a message or attach a photo to send."
        )
        return

    # List of user chat IDs to broadcast the message to
    user_chat_ids = [
        TEST_ID_1,
        TEST_ID_2,
    ]  # Replace with actual chat IDs

    # If a photo is attached, send the photo with the caption
    if update.message.photo:
        photo = update.message.photo[
            -1
        ].file_id  # Use the highest resolution photo available
        for chat_id in tqdm(
            user_chat_ids, desc="Sending photo and message", unit="user"
        ):
            try:
                await context.bot.send_photo(
                    chat_id=chat_id, photo=photo, caption="Photo from admin"
                )
                await context.bot.send_message(chat_id, message, parse_mode="Markdown")
                await context.bot.send_message(chat_id, "Photo and message sent.")
            except Exception as e:
                print(f"Failed to send photo and message to {chat_id}: {e}")
                await context.bot.send_message(
                    chat_id, "Failed to send photo and message."
                )

    else:
        # If no photo, send the message only
        for chat_id in tqdm(user_chat_ids, desc="Sending messages", unit="user"):
            try:
                await context.bot.send_message(chat_id, message, parse_mode="Markdown")
                await context.bot.send_message(chat_id, "Message sent.")
            except Exception as e:
                print(f"Failed to send message to {chat_id}: {e}")
                await context.bot.send_message(chat_id, "Failed to send message.")
