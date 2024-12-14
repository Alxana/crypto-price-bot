from telegram.ext import ContextTypes
from utils.utils import get_price
from utils.message_utils import format_price_update_message
from bots.base_bot import BaseBot
from utils.logger import logger
from configs.config import UPDATE_FREQUENCY


class CryptoPriceBot(BaseBot):
    def __init__(self, token: str, channel_id: str, currencies: list, api: str):
        super().__init__(token, channel_id)
        self.currencies = currencies
        self.api = api

    async def send_prices(self, chat_id):
        """
        Fetch and send cryptocurrency prices to the specified chat ID.
        """
        logger.info("Fetching prices...")
        messages = []
        for currency in self.currencies:
            price = get_price(currency, self.api)
            if price:
                messages.append(format_price_update_message(price))
            else:
                messages.append(f"Failed to fetch price for {currency}.")

        if messages:
            logger.info(f"Sending messages to chat {chat_id}...")
            await self.application.bot.send_message(
                chat_id=chat_id,
                text="\n".join(messages),
                parse_mode='Markdown'
            )
            logger.info("Prices sent successfully!")
        else:
            logger.warning("No messages to send.")

    async def run_single_update(self):
        """
        Perform a single run to fetch and send prices.
        """
        logger.info("Running single update...")
        await self.send_prices(chat_id=self.channel_id)
        logger.info("Single update completed.")

    async def periodic_updates(self, context: ContextTypes.DEFAULT_TYPE):
        """
        Job to periodically fetch and send prices.
        """
        logger.info("Running periodic updates...")
        await self.send_prices(chat_id=self.channel_id)

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