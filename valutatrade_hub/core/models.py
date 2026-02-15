import hashlib
import uuid
from datetime import datetime
from typing import Dict, List

from valutatrade_hub.core.exceptions import InsufficientFundsError


class Wallet:
    def __init__(self, currency: str, balance: float = 0.0):
        self.currency = currency
        self._balance = float(balance)

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        if amount > self._balance:
            raise InsufficientFundsError(f"Not enough {self.currency}")
        self._balance -= amount

    def to_dict(self):
        return {"currency": self.currency, "balance": self._balance}


class Portfolio:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self._wallets: Dict[str, Wallet] = {}

    def get_wallet(self, currency: str) -> Wallet:
        if currency not in self._wallets:
            self._wallets[currency] = Wallet(currency)
        return self._wallets[currency]

    @property
    def wallets(self) -> List[Wallet]:
        return list(self._wallets.values())

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "wallets": {curr: w.to_dict() for curr, w in self._wallets.items()}
        }
    
    @classmethod
    def from_dict(cls, data):
        pf = cls(data["user_id"])
        for curr, w_data in data.get("wallets", {}).items():
            pf._wallets[curr] = Wallet(curr, w_data["balance"])
        return pf


class User:
    def __init__(self, username: str, password: str, uid: str = None):
        self.username = username
        self.uid = uid or str(uuid.uuid4())
        self.created_at = datetime.now().isoformat()
        # Хеширование пароля (соль + sha256)
        if len(password) < 64: # Если не похоже на хеш
            self._password = self._hash_password(password)
        else:
            self._password = password

    def _hash_password(self, raw_password: str) -> str:
        salt = "static_salt_m25" # В идеале соль уникальна
        return hashlib.sha256((raw_password + salt).encode()).hexdigest()

    def check_password(self, raw_password: str) -> bool:
        return self._password == self._hash_password(raw_password)
    
    @property
    def password_hash(self):
        return self._password

    def to_dict(self):
        return {
            "uid": self.uid,
            "username": self.username,
            "password": self._password,
            "created_at": self.created_at
        }