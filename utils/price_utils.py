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


def format_prices(prices, max_length=7):
    formatted_prices = []
    for price in prices:
        formatted_prices.append(format_price(price, max_length))
    return formatted_prices


def format_price(price, max_length=7):
    formatted_prices = []
    # Convert to string and remove the decimal point
    str_price = f"{price:.15f}".rstrip("0").rstrip(".")
    # Keep at most 'max_length' characters
    if len(str_price) <= max_length:
        formatted_price = str_price
    else:
        # Truncate to max_length, ensuring there's a decimal point
        before_decimal, _, after_decimal = str_price.partition(".")
        truncated = before_decimal[:max_length]
        remaining = max_length - len(truncated) - 1  # Subtract for the decimal point
        if remaining > 0:
            truncated += "." + after_decimal[:remaining]
        formatted_price = truncated
    return formatted_price
