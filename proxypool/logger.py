from .config import BASE_DIR, LOG_LEVEL, LOG_FILE

from datetime import datetime
import logging
import logging.handlers
import os
import sys


def Logger():
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logger.setLevel(level=LOG_LEVEL)

    # Handler -> stream
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if not LOG_FILE:
        return logger

    # Handler -> file
    log_dir = os.path.join(BASE_DIR, "logs/")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename="logs/app",
        when="D",
        interval=60 * 60 * 24  # one day
    )
    file_handler.suffix = "%Y-%m-%d.log"
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


logger = Logger()
