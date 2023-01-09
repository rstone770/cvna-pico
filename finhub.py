from time import time
from lib.urequests import get

class Quote:
    def __init__(self,symbol: str, price: float, delta: float, percentage: float):
        self.symbol = symbol
        self.price = price
        self.delta = delta
        self.percentage = percentage
        self.requested_on = time()

class Finhub:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://finnhub.io/api/v1"

    def get_quote(self, symbol):
        token = self._getTokenParam()
        url = f"{self.base_url}/quote?{token}&symbol={symbol}"
        response = get(url)

        if response.status_code != 200:
            raise Exception(f"Finhub.GetQuote returned {response.status_code}.")

        json = response.json()

        return Quote(
            symbol,
            json['c'],
            json['d'],
            json["dp"])

    def _getTokenParam(self):
        return f"token={self.api_key}"
