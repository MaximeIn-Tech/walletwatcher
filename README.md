# Wallet Watcher Bot

**WalletWatcherBot** is a Telegram bot that aims to track crypto wallets and send notifications when cryptos are received or withdrawn.

## Technologies used

- Python 3.8 or higher
- Windows, macOS, or Linux operating system
- Python-telegram-bot as a library
- Multiple APIs
- **Supabase** to store data

## Usage

The bot is quite simple to use.

You follow the prompts:

- Enter a wallet address
- Choose a blockchain to track your cryptos on.
- Choose a token or enter one.
- Enter a trigger point.
- Enjoy!

The trigger point is the amount of tokens you want to trigger your alert.
It works for both positive and negative change.

For example, if your trigger point is 100 and the wallet receives 90 tokens, an alert won't be sent.
However, if the wallet withdraws 110 tokens, an alert will be sent.

Finally, the bot is localised for 3 languges.

## Lessons learned

This bot is the first big project that I create on my own from scratch.

It starte at first with a need to scratch my own itch.

I ended up creating a full bot that will, I hope, help people.

## Read More about the project here

https://medium.com/@itstechsherpa/i-created-a-telegram-bot-to-monitor-any-crypto-wallet-using-python-510758b1c6aa

## Change Log

### February 4th 2025:

- Add Solana and Ton as blockchains
