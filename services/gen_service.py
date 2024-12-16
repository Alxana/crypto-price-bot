import requests
from utils.utils import get_first_symbol_from_pair, get_second_symbol_from_pair, get_crypto_name_by_symbol


class ApiService:
    def __init__(self, currency_pairs):
        self.currency_pairs = currency_pairs

    # Mass fetch prices converted to one currency (default = USD)
    def fetch_prices(self):
        raise NotImplementedError("Subclasses must implement this method.")

    @staticmethod
    def make_http_request(url, headers, params):
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_symbol(self, currency_pair):
        return get_first_symbol_from_pair(currency_pair)

    def get_convert_to_symbol(self, currency_pair):
        return get_second_symbol_from_pair(currency_pair)

    def get_name(self, symbol):
        return get_crypto_name_by_symbol(symbol)

