import requests
import os
from .gen_service import ApiService
from configs.config import CMC_API_BASE_URL, CMC_LATEST_ENDPOINT, DEFAULT_CONVERT_TO_CURRENCY
from configs.config import CMC_API_KEY_HEADER
from utils.utils import load_cmc_id_mapping
from utils.logger import logger


class CoinMarketCapService(ApiService):
    def __init__(self, currency_pairs):
        super().__init__(currency_pairs)
        self.latest_url = f"{CMC_API_BASE_URL}{CMC_LATEST_ENDPOINT}"
        self.headers = {CMC_API_KEY_HEADER: self.get_api_key()}

    def get_api_key(self):
        # Attempt to import local secrets
        try:
            from configs.secrets_config import (
                CMC_API_KEY as LOCAL_CMC_API_KEY
            )
        except ImportError:
            # Define local variables as None if `secrets_config.py` is missing
            LOCAL_CMC_API_KEY = None

        # Use environment variables if available, otherwise fallback to local secrets
        return os.getenv("CMC_API_KEY", LOCAL_CMC_API_KEY)

    def get_cmc_id(self, pair):
        mapping = load_cmc_id_mapping()
        symbol = self.get_symbol(pair)
        return mapping[symbol]

    def fetch_prices(self):
        """
        Fetch price data from Binance API.
        :return: A list of dictionaries with coin data (symbol, price, and price changes).
        """
        ids = []
        for pair in self.currency_pairs:
            curr_id = self.get_cmc_id(pair)
            if curr_id:
                ids.append(curr_id)

        if not ids:
            logger.warn("No valid IDs were retrieved for the given currency pairs.")
            return []

        try:
            # Prepare parameters for the API request
            params = {"id": ",".join(map(str, ids))}
            latest_response = self.make_http_request(self.latest_url, self.headers, params=params)
            data = latest_response.get("data", {})

            if not isinstance(data, dict):
                logger.warn("Invalid response structure: 'data' should be a dictionary.")
                return []

            # Process each cryptocurrency data item
            results = []
            for crypto_id, crypto_data in data.items():
                parsed_item = self.parse_data_item(crypto_data)
                if parsed_item:  # Only append valid parsed items
                    results.append(parsed_item)

            return results

        except Exception as e:
            logger.error(f"An error occurred while fetching prices: {e}")
            return []

    def parse_data_item(self, crypto_data):
        if not isinstance(crypto_data, dict):
            # Return None if crypto_data is not a valid dictionary
            logger.error("Invalid crypto_data format: expected a dictionary.")
            return None

        # Extract symbol
        symbol = crypto_data.get("symbol")
        if not symbol:
            # Log and skip if symbol is missing
            logger.error("Missing 'symbol' in crypto_data.")
            return None

        # Extract the quote data for USD or specified currency
        quote = crypto_data.get("quote", {}).get(DEFAULT_CONVERT_TO_CURRENCY, {})
        if not isinstance(quote, dict):
            logger.error(f"Invalid 'quote' format for symbol: {symbol}")
            return None

        # Extract specific fields with fallback to None
        price = quote.get("price")
        percent_change_24h = quote.get("percent_change_24h")
        percent_change_7d = quote.get("percent_change_7d")

        # Return parsed data
        return {
            "symbol": symbol,
            "convert_to": DEFAULT_CONVERT_TO_CURRENCY,
            "price": price,
            "percent_change_24h": percent_change_24h,
            "percent_change_7d": percent_change_7d
        }
