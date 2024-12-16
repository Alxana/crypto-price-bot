import requests
from .gen_service import ApiService
from configs.config import BINANCE_API_BASE_URL, BINANCE_PRICE_ENDPOINT
from utils.logger import logger


class BinanceService(ApiService):
    def __init__(self, currency_pair):
        super().__init__(currency_pair)
        self.url = f"{BINANCE_API_BASE_URL}{BINANCE_PRICE_ENDPOINT}"

    def fetch_price(self):
        """
        Fetch price data from Binance API.
        :return: A JSON object with coin, current price, and price change.
        """
        try:
            # Split the pair into base and quote currencies (e.g., "BNB-BTC" -> "BNB", "BTC")
            base_currency, quote_currency = self.currency_pair.split("-")
            symbol = f"{base_currency.upper()}{quote_currency.upper()}"

            # Make the request to Binance API
            params = {"symbol": symbol}
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            data = response.json()

            # Parse the response
            current_price = float(data.get("lastPrice", 0.0))
            price_change_24h = float(data.get("priceChangePercent", 0.0))

            return {
                "coin": self.currency_pair,
                "currentPrice": current_price,
                "priceChange24": price_change_24h
            }
        except (requests.RequestException, KeyError, ValueError) as e:
            logger.error(f"Error fetching data from Binance: {e}")
            return None
