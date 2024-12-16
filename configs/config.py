# API URLs
COINBASE_API_BASE_URL = 'https://api.coinbase.com'
COINBASE_PRICE_ENDPOINT = "/v2/prices"

GECKO_API_BASE_URL = "https://api.coingecko.com/api/v3"
GECKO_PRICE_ENDPOINT = "/simple/price"

BINANCE_API_BASE_URL = "https://api.binance.com/api/v3"
BINANCE_PRICE_ENDPOINT = "/ticker/24hr"

CMC_API_BASE_URL = "https://pro-api.coinmarketcap.com"
CMC_LATEST_ENDPOINT = "/v2/cryptocurrency/quotes/latest"

# Defaults
DEFAULT_API = "cmc"
DEFAULT_TRACKED_CURRENCIES = ["TON-USDT", "TRX-USDT", "BTC-USDT"]
DEFAULT_CONVERT_TO_CURRENCY = "USD"

# Update frequency (in sec)
UPDATE_FREQUENCY = 1800
