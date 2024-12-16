import json


def load_crypto_mapping(file_path="configs/crypto_symbol_name_mapping.json"):
    with open(file_path, "r") as f:
        return json.load(f)


def load_cmc_id_mapping(file_path="configs/crypto_symbol_cmc_id_mapping.json"):
    with open(file_path, "r") as f:
        return json.load(f)


def get_crypto_name_by_symbol(symbol):
    mapping = load_crypto_mapping()
    return mapping.get(symbol, "Unknown symbol")


def get_first_symbol_from_pair(currency_pair):
    # Split the pair into base and quote currencies (e.g., "BNB-BTC" -> "BNB", "BTC")
    # and returns base one
    base_currency, quote_currency = currency_pair.split("-")
    return f"{base_currency.upper()}"


def get_second_symbol_from_pair(currency_pair):
    # Split the pair into base and quote currencies (e.g., "BNB-BTC" -> "BNB", "BTC")
    # and returns quote one
    base_currency, quote_currency = currency_pair.split("-")
    return f"{quote_currency.upper()}"
