import requests

from valutatrade_hub.logging_config import logger
from valutatrade_hub.parser_service.config import BASE_URL


class BaseApiClient:
    def fetch_rates(self):
        raise NotImplementedError

class ExchangeRateClient(BaseApiClient):
    def fetch_rates(self):
        try:
            logger.info(f"Fetching rates from {BASE_URL}")
            resp = requests.get(BASE_URL, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return data.get("rates", {})
        except Exception as e:
            logger.error(f"API Error: {e}")
            # Возвращаем заглушку если нет инета
            return {"USD": 1.0, "EUR": 0.92, "RUB": 91.5, "GBP": 0.79}