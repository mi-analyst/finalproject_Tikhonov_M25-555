import json
import os
from valutatrade_hub.infra.settings import settings

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def _load_json(self, path):
        if not os.path.exists(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _save_json(self, path, data):
        # Атомарная запись (пишем во временный, потом переименовываем)
        tmp_path = f"{path}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        os.replace(tmp_path, path)

    # --- Users ---
    def load_users(self):
        return self._load_json(settings.USERS_FILE)

    def save_users(self, data):
        self._save_json(settings.USERS_FILE, data)

    # --- Portfolios ---
    def load_portfolios(self):
        return self._load_json(settings.PORTFOLIOS_FILE)

    def save_portfolios(self, data):
        self._save_json(settings.PORTFOLIOS_FILE, data)
        
    # --- Rates (КЭШ) ---
    def load_rates(self):
        return self._load_json(settings.RATES_FILE)
    
    def save_rates(self, data):
        self._save_json(settings.RATES_FILE, data)

    # --- History (ИСТОРИЯ) ---
    def load_history(self):
        return self._load_json(settings.HISTORY_FILE)

    def save_history(self, data):
        self._save_json(settings.HISTORY_FILE, data)

db = DatabaseManager()