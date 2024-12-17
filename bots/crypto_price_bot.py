from telegram.error import TelegramError
from telegram.ext import ContextTypes
from utils.price_utils import get_price
from utils.message_utils import format_price_update_message
from bots.base_bot import BaseBot
from utils.logger import logger
from configs.config import UPDATE_FREQUENCY


class CryptoPriceBot(BaseBot):
    def __init__(self, token: str, channel_ids: list, currencies: list, api: str):
        super().__init__(token, channel_ids)
        self.currencies = currencies
        self.api = api

    from telegram.error import TelegramError

    async def send_prices(self, chat_id):
        """
        Fetch and send cryptocurrency prices to the specified chat ID.
        """
        logger.info("Fetching prices...")
        messages = []
        prices = get_price(self.currencies, self.api)

        for price in prices:
            if price:
                messages.append(format_price_update_message(price))
            else:
                messages.append(f"Failed to fetch price for {price['symbol']}-{price['convert_to']}.")

        if messages:
            try:
                logger.info(f"Sending messages to chat {chat_id}...")
                await self.application.bot.send_message(
                    chat_id=chat_id,
                    text="\n".join(messages),
                    parse_mode='Markdown'
                )
                logger.info("Prices sent successfully!")
            except TelegramError as e:
                # Log the error and continue execution
                logger.warning(f"Failed to send message to chat {chat_id}. Error: {e}")
        else:
            logger.warning("No messages to send.")

    async def run_single_update(self):
        """
        Perform a single run to fetch and send prices.
        """
        logger.info("Running single update...")
        for channel in self.channel_ids:
            await self.send_prices(chat_id=channel)
        logger.info("Single update completed.")

    async def periodic_updates(self, context: ContextTypes.DEFAULT_TYPE):
        """
        Job to periodically fetch and send prices.
        """
        logger.info("Running periodic updates...")
        for channel in self.channel_ids:
            await self.send_prices(chat_id=channel)
        logger.info("Periodic update completed...")

    def run_periodic_updates(self):
        """
        Schedule and run periodic updates.
        """
        logger.info("Setting up periodic updates...")
        self.setup()  # Set up handlers from the parent class

        # Schedule periodic updates to the channel
        job_queue = self.application.job_queue
        job_queue.run_repeating(self.periodic_updates, interval=UPDATE_FREQUENCY, first=3)
        logger.info("Periodic updates scheduled!")

        # Start the polling loop
        self.run_polling()