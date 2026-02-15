from functools import wraps

from valutatrade_hub.logging_config import logger


def log_action(func):
    """Decorator to log user actions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"Action started: {func.__name__}")
            result = func(*args, **kwargs)
            logger.info(f"Action finished: {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper