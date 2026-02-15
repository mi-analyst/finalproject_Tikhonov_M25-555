import logging
import sys
from logging.handlers import RotatingFileHandler


def setup_logging():
    """Configures application-wide logging."""
    logger = logging.getLogger("ValutaTrade")
    logger.setLevel(logging.INFO)

    # Формат
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Файл с ротацией
    file_handler = RotatingFileHandler("app.log", maxBytes=1024*1024, backupCount=3)
    file_handler.setFormatter(formatter)
    
    # Консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()