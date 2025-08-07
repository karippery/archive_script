import logging
from logging.handlers import RotatingFileHandler


def get_logger(log_file):
    logger = logging.getLogger("ArchiveLogger")
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger
