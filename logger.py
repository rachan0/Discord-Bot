# logger.py

import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(
        filename='bot.log',
        encoding='utf-8',
        mode='a',
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=5
    )
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
