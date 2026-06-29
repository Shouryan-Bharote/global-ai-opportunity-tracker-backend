import logging

from shared.config import settings
from shared.constants.logging import LOGGER_NAME
from shared.logger.handlers import get_console_handler

def _create_logger() -> logging.Logger:
    """
    Create and configure the application's root logger.
    """

    logger = logging.getLogger(LOGGER_NAME)

    # Prevent duplicate handlers if imported multiple times
    if logger.handlers:
        return logger

    logger.setLevel(settings.log_level)

    logger.addHandler(get_console_handler())
    logger.propagate = False

    return logger



logger = _create_logger()