class TradeHubError(Exception):
    """Base exception for the app."""
    pass

class InsufficientFundsError(TradeHubError):
    pass

class UserAlreadyExistsError(TradeHubError):
    pass

class AuthenticationError(TradeHubError):
    pass

class CurrencyNotFoundError(TradeHubError):
    pass