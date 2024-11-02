import asyncio
import logging
from datetime import datetime

from dotenv import load_dotenv
from httpcore import ConnectError
from telegram import Bot

from database import *
from wallets import *

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="logs.log",
    encoding="utf-8",
    filemode="a",
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

token = os.getenv("TELEGRAM_BOT_TOKEN")


async def check_balance():

    bot = Bot(token)

    # Connect to the database
    supabase = connect_to_database()
    # Recover all the setups except stake watch

    blockchain_sleep_times = {
        "ETH": 0.1,
        "BSC": 0.1,
        "THETA": 0.5,
    }

    try:
        fetched_setups = (
            supabase.table("Setups")
            .select("*", count="exact")
            .neq("token_symbol", "Stake Watch")
            .execute()
        )

        if fetched_setups:
            fetched_setups = fetched_setups.data
            for setup in fetched_setups:
                balance_in_db = setup["balance"]
                new_balance = fetch_wallet_balance(
                    setup["blockchain"],
                    setup["token_symbol"],
                    setup["wallet_address"],
                    setup["contract_address"],
                )
                id = setup["id"]
                if new_balance is not None and balance_in_db is not None:
                    new_balance = round(new_balance, 2)
                    delta = new_balance - balance_in_db
                    delta = round(delta, 2)
                    wallet_name = await fetch_wallet_address(setup["wallet_address"])
                    wallet_name = wallet_name.data
                    name = wallet_name[0]["wallet_name"]
                    data = (
                        supabase.table("Setups")
                        .update({"balance": new_balance})
                        .eq("id", id)
                        .execute()
                    )
                    if delta == 0:
                        # print("Next iteration, delta = 0")
                        continue
                    # elif delta < setup["trigger_point"]:
                    #     print("Next iteration, delta < trigger point.")
                    #     continue
                    else:
                        user_language = await get_language_for_chat_id(setup["chat_id"])
                        if delta > 0 and delta > setup["trigger_point"]:
                            # French message
                            if user_language == "fr":
                                await bot.send_message(
                                    chat_id=setup["chat_id"],
                                    text=f"📈 Le portefeuille nommé {name} a reçu :\n{delta}{setup['token_symbol']}.\nVotre solde est maintenant de {new_balance} {setup['token_symbol']}.",
                                    disable_notification=True,
                                )
                            # Spanish message
                            elif user_language == "es":
                                await bot.send_message(
                                    chat_id=setup["chat_id"],
                                    text=f"📈 La billetera llamada {name} recibió:\n{delta}{setup['token_symbol']}.\nTu saldo es ahora {new_balance} {setup['token_symbol']}.",
                                    disable_notification=True,
                                )
                            else:
                                await bot.send_message(
                                    chat_id=setup["chat_id"],
                                    text=f"📈 Wallet named {name} received:\n{delta}{setup['token_symbol']}.\nYour balance is now {new_balance} {setup['token_symbol']}.",
                                    disable_notification=True,
                                )
                        elif delta < 0 and delta < -setup["trigger_point"]:
                            # French message
                            if user_language == "fr":
                                await bot.send_message(
                                    chat_id=setup["chat_id"],
                                    text=f"📉 Le portefeuille nommé {name} a retiré :\n{delta}{setup['token_symbol']}.\nVotre solde est maintenant de {new_balance} {setup['token_symbol']}.",
                                    disable_notification=True,
                                )
                            # Spanish message
                            elif user_language == "es":
                                await bot.send_message(
                                    chat_id=setup["chat_id"],
                                    text=f"📉 La billetera llamada {name} retiró:\n{delta}{setup['token_symbol']}.\nTu saldo es ahora {new_balance} {setup['token_symbol']}.",
                                    disable_notification=True,
                                )
                            else:
                                await bot.send_message(
                                    chat_id=setup["chat_id"],
                                    text=f"📉 Wallet named {name} withdrew:\n{delta}{setup['token_symbol']}.\nYour balance is now {new_balance} {setup['token_symbol']}.",
                                    disable_notification=True,
                                )
                            # logger.info(f"Message sent for withdrawn tokens to {setup["chat_id"]}")
                else:
                    pass
                blockchain_sleep_time = blockchain_sleep_times.get(
                    setup["blockchain"], 0.5
                )
                await asyncio.sleep(blockchain_sleep_time)
    except Exception as e:
        print("An error occurred:", e)
        return None  # Return None in case of any errors


async def check_stake_watch():
    bot = Bot(token)
    # Connect to the database
    supabase = connect_to_database()
    # Recover all the stake watch setups
    try:
        fetched_setups_from_db = (
            supabase.table("Setups")
            .select("*", count="exact")
            .eq("token_symbol", "Stake Watch")
            .execute()
        )
        fetched_setups_from_db = fetched_setups_from_db.data

        if fetched_setups_from_db:
            for setup in fetched_setups_from_db:
                id = setup["id"]
                stake_data = setup["stake_data"]
                nodes = stake_data["sourceRecords"]
                if nodes:
                    wallet_name = await fetch_wallet_address(setup["wallet_address"])
                    wallet_name = wallet_name.data
                    name = wallet_name[0]["wallet_name"]
                    withdrawn_values_from_db = []
                    withdrawn_values_from_api = []
                    for item in nodes:
                        withdrawn_values_from_db.append(item["withdrawn"])
                    # print (withdrawn_values_from_db)
                    current_stakes = fetch_stake_for_wallet(setup["wallet_address"])
                    data = (
                        supabase.table("Setups")
                        .update({"stake_data": current_stakes})
                        .eq("id", id)
                        .execute()
                    )
                    current_stakes_values = current_stakes["sourceRecords"]
                    for item in current_stakes_values:
                        withdrawn_values_from_api.append(item["withdrawn"])
                    if any(withdrawn_values_from_api):
                        if withdrawn_values_from_api != withdrawn_values_from_db:
                            user_language = await get_language_for_chat_id(
                                setup["chat_id"]
                            )
                            # French message
                            if user_language == "fr":
                                await bot.send_message(
                                    chat_id=setup["chat_id"],
                                    text=f"🔥 ALERTE : Un stake de votre portefeuille *{name}* est en cours de retrait ! 🔥\nSi cette action n'est pas la vôtre, agissez MAINTENANT et sécurisez votre portefeuille ! 🔒",
                                    parse_mode="Markdown",
                                    disable_notification=True,
                                )
                            # Spanish message
                            elif user_language == "es":
                                await bot.send_message(
                                    chat_id=setup["chat_id"],
                                    text=f"🔥 ¡ALERTA: Se está retirando una apuesta de tu billetera *{name}*! 🔥\nSi esta acción no es tuya, ¡actúa AHORA y asegura tu billetera! 🔒",
                                    parse_mode="Markdown",
                                    disable_notification=True,
                                )
                            else:
                                await bot.send_message(
                                    chat_id=setup["chat_id"],
                                    text=f"🔥 ALERT: A stake from your *{name}* wallet is being withdrawn! 🔥\nIf this action isn't yours, act NOW and secure your wallet! 🔒",
                                    parse_mode="Markdown",
                                    disable_notification=True,
                                )
                            logger.info(
                                f"Message sent for stake alert to {setup['chat_id']}"
                            )
                        else:
                            continue
                    else:
                        continue
                else:
                    print("No records.")
                    continue
                await asyncio.sleep(1)
    except Exception as e:
        print("An error occurred:", e)
        return None  # Return None in case of any errors


if __name__ == "__main__":
    # Set intervals for each function
    check_balance_interval = 600  # in seconds
    check_stake_watch_interval = 3600  # in seconds

    async def check_balance_loop():
        while True:
            now = datetime.now()
            print(f"{now} Running check_balance...")
            await check_balance()
            now = datetime.now()
            print(f"{now} Completed check_balance.")
            await asyncio.sleep(check_balance_interval)

    async def check_stake_watch_loop():
        while True:
            now = datetime.now()
            print(f"{now} Running check_stake_watch...")
            await check_stake_watch()
            now = datetime.now()
            print(f"{now} Completed check_stake_watch.")
            await asyncio.sleep(check_stake_watch_interval)

    # Start the event loop for each function
    async def main():
        await asyncio.gather(check_balance_loop(), check_stake_watch_loop())

    asyncio.run(main())
