from services.binance_service import BinanceService
from services.gecko_service import GeckoService
from services.coinmarketcap_service import CoinMarketCapService
from .logger import logger

API_SERVICES = {
    "gecko": GeckoService,
    "binance": BinanceService,
    "cmc": CoinMarketCapService
    # Add other APIs like "kraken" here
}


def get_price(currency_pairs, api_name):
    """
    Fetch the current price for the given currency pair from the specified API.
    :param currency_pairs: An array of strings representing the currency pairs requested, e.g., ["BNB-BTC", "TRX-USD"].
    :param api_name: A string representing the API name, e.g., "coinbase" or "gecko".
    :return: A dictionary with the coin, current price, and 24h price change, or None if the request fails.
    """
    api_service_class = API_SERVICES.get(api_name.lower())
    if not api_service_class:
        logger.warn(f"Unsupported API: {api_name}")
        return None
    api_service = api_service_class(currency_pairs)

    try:
        return api_service.fetch_prices()
    except Exception as e:
        logger.error(f"Error fetching price from {api_name}: {e}")
        return None
