import logging
import logging.config
import os
from datetime import datetime
from app.config import get_settings

settings = get_settings()

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": settings.log_level,
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": settings.log_level,
            "formatter": "detailed",
            "filename": f"logs/app_{datetime.now().strftime('%Y%m%d')}.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "detailed",
            "filename": f"logs/errors_{datetime.now().strftime('%Y%m%d')}.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "app": {
            "level": settings.log_level,
            "handlers": ["console", "file", "error_file"],
            "propagate": False,
        },
    },
    "root": {
        "level": settings.log_level,
        "handlers": ["console", "file"],
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a given module name"""
    return logging.getLogger(f"app.{name}")
