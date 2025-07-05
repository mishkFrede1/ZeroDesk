import logging
import os

LOG_LEVEL = os.environ["LOG_LEVEL"].upper()
def get_logger(name=""):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(asctime)s] - [%(levelname)s] - [%(name)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(LOG_LEVEL)

        logger.propagate = False

    return logger

