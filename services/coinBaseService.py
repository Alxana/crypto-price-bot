import requests


def fetch_crypto_prices():
    url = "https://api.coinbase.com/v2/prices"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        # Parse and return the relevant prices
        return data
    else:
        raise Exception("Failed to fetch data")
