import time
from valutatrade_hub.parser_service.api_clients import ExchangeRateClient
from valutatrade_hub.infra.database import db
from valutatrade_hub.logging_config import logger

class RatesUpdater:
    def __init__(self):
        self.client = ExchangeRateClient()

    def run_update(self):
        logger.info("Starting rates update...")
        rates = self.client.fetch_rates()
        
        if not rates:
            logger.warning("No rates fetched.")
            return

        # 1. Обновляем локальный кэш (rates.json)
        # ИСПОЛЬЗУЕМ МЕТОД db.save_rates ВМЕСТО ПРЯМОГО ДОСТУПА
        db.save_rates(rates)
        
        # 2. Обновляем историю (exchange_rates.json)
        history = db.load_history()
        timestamp = str(int(time.time()))
        history[timestamp] = rates
        db.save_history(history)
        
        logger.info("Rates updated successfully.")