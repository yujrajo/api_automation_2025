import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = "%(asctime)s UTC %(levelname)-8s %(name)-15s  %(message)s"


def get_logger(name, level=DEFAULT_LOG_LEVEL, log_format=DEFAULT_LOG_FORMAT) -> logging.Logger:
    """Method that returns the logger"""
    # path to log file, initialize file and console logger
    base_path = Path(__file__).parent.parent
    log_file_name = "asana.log"
    Path(f"{base_path}/logs").mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)

    for handler in logger.handlers:
        logger.removeHandler(handler)
    formatter = logging.Formatter(log_format)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(f"{base_path}/logs/{log_file_name}", maxBytes=5 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False
    logger.setLevel(level)

    return logger
