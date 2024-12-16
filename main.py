import os
import asyncio
from bots.crypto_price_bot import CryptoPriceBot
from configs.config import DEFAULT_TRACKED_CURRENCIES, DEFAULT_API
from utils.secrets_handling import return_secret, csv_secret_to_array

if __name__ == "__main__":

    token = return_secret("TELEGRAM_BOT_TOKEN")
    channel_ids = return_secret("CHANNEL_IDS")
    channel_ids = csv_secret_to_array(channel_ids) if isinstance(channel_ids, str) else channel_ids

    # Initialize and run the bot        
    crypto_bot = CryptoPriceBot(
        token=token,
        channel_ids=channel_ids,
        currencies=DEFAULT_TRACKED_CURRENCIES,
        api=DEFAULT_API
    )
    asyncio.run(crypto_bot.run_single_update())
