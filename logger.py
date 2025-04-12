import logging
import time
import json
from functools import wraps

def get_logger(name='clinIQ'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler("logs/flask-structured.log")
        formatter = logging.Formatter(json.dumps({
            "timestamp": "%(asctime)s",
            "level": "%(levelname)s",
            "message": "%(message)s",
            "source": "%(name)s"
        }))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

def log_timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            end = time.time()
            logger.info(f"{func.__name__} ran in {end - start:.2f}s")
    return wrapper
