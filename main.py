import os
import asyncio
from bots.cryptoPriceBot import CryptoPriceBot
from configs.config import DEFAULT_TRACKED_CURRENCIES, DEFAULT_API

if __name__ == "__main__":
    # Attempt to import local secrets
    try:
        from configs.secrets_config import (
            TELEGRAM_BOT_TOKEN as LOCAL_TELEGRAM_BOT_TOKEN,
            CHANNEL_ID as LOCAL_CHANNEL_ID
        )
    except ImportError:
        # Define local variables as None if `secrets_config.py` is missing
        LOCAL_TELEGRAM_BOT_TOKEN = None
        LOCAL_CHANNEL_ID = None

    # Use environment variables if available, otherwise fallback to local secrets
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", LOCAL_TELEGRAM_BOT_TOKEN)
    CHANNEL_ID = os.getenv("CHANNEL_ID", LOCAL_CHANNEL_ID)

    # Initialize and run the bot        
    crypto_bot = CryptoPriceBot(
        token=TELEGRAM_BOT_TOKEN,
        channel_id=CHANNEL_ID,
        currencies=DEFAULT_TRACKED_CURRENCIES,
        api=DEFAULT_API
    )
    asyncio.run(crypto_bot.run_single_update())
