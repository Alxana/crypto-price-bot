from services.binance_service import BinanceService
from services.gecko_service import GeckoService
from .logger import logger

API_SERVICES = {
    "gecko": GeckoService,
    "binance": BinanceService
    # Add other APIs like "binance", "kraken" here
}


def get_price(currency_pair, api_name):
    """
    Fetch the current price for the given currency pair from the specified API.
    :param currency_pair: A string representing the currency pair, e.g., "BNB-BTC".
    :param api_name: A string representing the API name, e.g., "coinbase" or "gecko".
    :return: A dictionary with the coin, current price, and 24h price change, or None if the request fails.
    """
    api_service_class = API_SERVICES.get(api_name.lower())
    if not api_service_class:
        logger.warn(f"Unsupported API: {api_name}")
        return None
    api_service = api_service_class()

    try:
        return api_service.fetch_price(currency_pair)
    except Exception as e:
        logger.error(f"Error fetching price from {api_name}: {e}")
        return None
