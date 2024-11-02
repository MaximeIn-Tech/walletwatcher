import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes

from database import *

load_dotenv()

ADMIN_ID = os.getenv("ADMIN_ID")  # Replace with your actual admin ID


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
        for user in users.data:
            chat_id = user["chat_id"]
            try:
                await context.bot.send_message(chat_id, message)
            except Exception as e:
                print(f"Could not send message to {chat_id}: {e}")

        await update.message.reply_text("Message sent to all users.")
    else:
        await update.message.reply_text("No registered users found.")


async def broadcast_message_test(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Send a photo with a message to all registered users."""
    print(f"Broadcast command received from {update.effective_user.id}")

    if str(update.effective_user.id) != ADMIN_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    # Extract the caption or message from the command
    message = update.message.text[len("/broadcast ") :].strip()
    if not message and not update.message.photo:
        await update.message.reply_text(
            "Please provide a message or attach a photo to send."
        )
        return

    # Test Chat ID for broadcasting
    TEST_CHAT_ID = "6269998887"  # Replace with actual chat ID

    # If a photo is attached, send the photo with the caption
    if update.message.photo:
        photo = update.message.photo[
            -1
        ].file_id  # Use the highest resolution photo available
        try:
            await context.bot.send_photo(
                chat_id=TEST_CHAT_ID, photo=photo, caption=message or "Photo from admin"
            )
            await update.message.reply_text("Photo and message sent to the test user.")
        except Exception as e:
            print(f"Failed to send photo and message: {e}")
            await update.message.reply_text(
                "Failed to send photo and message to the test user."
            )
    else:
        # If no photo, send the message only
        try:
            await context.bot.send_message(TEST_CHAT_ID, message)
            await update.message.reply_text("Message sent to the test user.")
        except Exception as e:
            print(f"Failed to send message: {e}")
            await update.message.reply_text("Failed to send message to the test user.")
