import requests
from configs.config import GECKO_API_BASE_URL


def fetch_price(currency_pair):
    """
    Fetch price data from CoinGecko API.
    :param currency_pair: A string representing the currency pair, e.g., "BNB-BTC".
    :return: A JSON object with coin, current price, and price change.
    """
    try:
        # Split pair for Gecko's format (e.g., "BNB-BTC" -> "binancecoin", "bitcoin")
        base_currency, quote_currency = currency_pair.split("-")
        params = {
            "ids": base_currency.lower(),
            "vs_currencies": quote_currency.lower(),
            "include_market_cap": "false",
            "include_24hr_change": "true"
        }
        response = requests.get(GECKO_API_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Parse the response
        current_price = data[base_currency.lower()][quote_currency.lower()]
        price_change_24h = data[base_currency.lower()].get("24h_change", 0)

        return {
            "coin": currency_pair,
            "currentPrice": current_price,
            "priceChange24": price_change_24h
        }
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Error fetching data from CoinGecko: {e}")
        return None


class GeckoService:
    pass
