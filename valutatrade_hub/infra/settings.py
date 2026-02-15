import os
from pathlib import Path


class SettingsLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsLoader, cls).__new__(cls)
            cls._instance._init_settings()
        return cls._instance

    def _init_settings(self):
        self.BASE_DIR = Path(__file__).parent.parent.parent
        self.DATA_DIR = self.BASE_DIR / "data"
        self.USERS_FILE = self.DATA_DIR / "users.json"
        self.PORTFOLIOS_FILE = self.DATA_DIR / "portfolios.json"
        self.RATES_FILE = self.DATA_DIR / "rates.json"
        self.HISTORY_FILE = self.DATA_DIR / "exchange_rates.json"
        
        # Конфигурация TTL (5 минут)
        self.CACHE_TTL = 300
        
        # Создаем папку data если нет
        os.makedirs(self.DATA_DIR, exist_ok=True)

settings = SettingsLoader()