async def main_menu_message(username):
    return f"""🚀 Welcome to Crypto Wallet Monitor {username}, crafted with care by @TechSherpa!

Ready to stay in the loop with real-time alerts whenever transactions occur in your crypto wallets? Let's get started!

With this intuitive bot, you can handpick wallets from various blockchains, set your preferences, and stay in the loop with updates precisely when you desire.

Explore our suite of commands:
"""


async def add_wallet_start_message():
    return """Please add a wallet:
"""


async def settings_message():
    return """Please choose a setting you want to adjust:
"""


async def help_message():
    return """The bot attentively processes your inquiries and securely stores your data within a database. 
    
Maintaining user anonymity is paramount; hence, only your Chat_ID is retained, ensuring precise message delivery without intertwining data from various users. 
    
Additionally, the bot refrains from logging your IP, username, or any other details that could potentially identify you as a user.
"""


async def language_selection_message():
    return """Please choose a language you prefer:
    """


async def stake_message():
    return """Stakes on this wallet are being watched. You'll be notified if a stake is withdrawn.
    """
