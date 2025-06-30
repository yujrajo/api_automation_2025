import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = "%(asctime)s UTC %(levelname)-8s %(name)-15s  %(message)s"
LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def get_logger(name, level:str =DEFAULT_LOG_LEVEL, log_format:str=DEFAULT_LOG_FORMAT) -> logging.Logger:
    """Method that configures and returns the logger instance

    Args:
        name (_type_): Name of the module that call the logger
        level (str, optional): Log level.Accepted values: DEBUG", "INFO", "WARNING", "ERROR" and "CRITICAL".
                               Defaults to DEFAULT_LOG_LEVEL.
        log_format (str, optional): Format of the displayed log. Defaults to DEFAULT_LOG_FORMAT.

    Returns:
        logging.Logger: Logger instance
    """
    # path to log file, initialize file and console logger
    base_path = Path(__file__).parent.parent
    log_file_name = "asana.log"
    Path(f"{base_path}/logs").mkdir(parents=True, exist_ok=True)
    # create logger
    logger = logging.getLogger(name)
    # remove other handlers
    for handler in logger.handlers:
        logger.removeHandler(handler)
    formatter = logging.Formatter(log_format)
    # set console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    # set file handler
    file_handler = RotatingFileHandler(f"{base_path}/logs/{log_file_name}", maxBytes=5 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(formatter)
    # add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False
    logger.setLevel(LEVELS[level])

    return logger
