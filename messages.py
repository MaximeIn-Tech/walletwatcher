async def main_menu_message():
    return """🚀 Welcome to Crypto Wallet Monitor, crafted with care by @TechSherpa!

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
    return """The bot is listening to your queries and stores your data in a database.

An important thing for me is to keep users anonymous so the only thing that is kept is your Chat_ID with the bot.
In that, he will know who to send messages to and not mix up the data from everyone.

Other than that, the bot doesn't log:
    - Your IP
    - Your username
    - Any other information that would identify you as a user.
"""


async def language_selection_message():
    return """Please choose a language you prefer:
    """
