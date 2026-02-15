from valutatrade_hub.core.exceptions import AuthenticationError, CurrencyNotFoundError, UserAlreadyExistsError
from valutatrade_hub.core.models import Portfolio, User
from valutatrade_hub.decorators import log_action
from valutatrade_hub.infra.database import db


class AuthManager:
    def register(self, username, password):
        users_data = db.load_users()
        for u in users_data.values():
            if u["username"] == username:
                raise UserAlreadyExistsError("Username taken")
        
        new_user = User(username, password)
        users_data[new_user.uid] = new_user.to_dict()
        db.save_users(users_data)
        
        # Создаем пустой портфель
        pf_data = db.load_portfolios()
        pf = Portfolio(new_user.uid)
        pf_data[new_user.uid] = pf.to_dict()
        db.save_portfolios(pf_data)
        
        return new_user

    def login(self, username, password):
        users_data = db.load_users()
        for u_data in users_data.values():
            if u_data["username"] == username:
                user = User(u_data["username"], u_data["password"], u_data["uid"])
                if user.check_password(password):
                    return user
        raise AuthenticationError("Invalid credentials")


class TradingService:
    def __init__(self, user: User):
        self.user = user
        self.pf = self._load_portfolio()
        self.rates = db.load_rates()

    def _load_portfolio(self):
        data = db.load_portfolios()
        return Portfolio.from_dict(data.get(self.user.uid))

    def _save_portfolio(self):
        data = db.load_portfolios()
        data[self.user.uid] = self.pf.to_dict()
        db.save_portfolios(data)

    @log_action
    def buy_currency(self, target_currency, amount_in_base, base_currency="USD"):
        """Покупка валюты за базовую (USD)."""
        rate = self.rates.get(target_currency)
        if not rate:
            raise CurrencyNotFoundError(f"Rate for {target_currency} not found")
        
        base_wallet = self.pf.get_wallet(base_currency)
        target_wallet = self.pf.get_wallet(target_currency)
        
        base_wallet.withdraw(amount_in_base)
        
        # Конвертация: amount_usd * rate (если rate это кол-во валюты за 1 USD)
        received_amount = amount_in_base * rate
        target_wallet.deposit(received_amount)
        
        self._save_portfolio()
        return received_amount

    def get_portfolio_value(self, base="USD"):
        total = 0.0
        details = []
        for wallet in self.pf.wallets:
            rate = self.rates.get(wallet.currency, 0)
            # Приводим к USD (обратная конвертация)
            if rate > 0:
                val_in_base = wallet.balance / rate
            else:
                val_in_base = 0
            
            total += val_in_base
            details.append((wallet.currency, wallet.balance, val_in_base))
        return total, details