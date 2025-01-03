import os
import asyncio
from bots.crypto_price_bot import CryptoPriceBot
from configs.config import DEFAULT_API
from utils.secrets_handling import return_secret, csv_secret_to_array

if __name__ == "__main__":

    token = return_secret("TELEGRAM_BOT_TOKEN")
    channel_ids = return_secret("CHANNEL_IDS")
    channel_ids = csv_secret_to_array(channel_ids) if isinstance(channel_ids, str) else channel_ids
    tracked_currencies = return_secret("TRACKED_CURRENCIES")
    tracked_currencies = csv_secret_to_array(tracked_currencies) if isinstance(tracked_currencies, str) else tracked_currencies

    # Initialize and run the bot        
    crypto_bot = CryptoPriceBot(
        token=token,
        channel_ids=channel_ids,
        currencies=tracked_currencies,
        api=DEFAULT_API
    )
    asyncio.run(crypto_bot.run_single_update())
