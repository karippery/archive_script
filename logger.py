import logging
from logging.handlers import RotatingFileHandler
from logging import LoggerAdapter


class RunIdAdapter(LoggerAdapter):
    def process(self, msg, kwargs):
        return f"[run_id={self.extra['run_id']}] {msg}", kwargs
    
def get_logger(log_file, run_id=None):
    logger = logging.getLogger("ArchiveLogger")
    logger.setLevel(logging.INFO)

    # Clear existing handlers to ensure consistent formatting
    logger.handlers.clear()

    handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    if run_id:
        return RunIdAdapter(logger, {"run_id": run_id})

    return logger

