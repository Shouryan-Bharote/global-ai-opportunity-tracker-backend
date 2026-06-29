import logging

from shared.logger.formatters import get_console_formatter


def get_console_handler() -> logging.Handler:
    handler = logging.StreamHandler()
    handler.setLevel(logging.NOTSET)
    handler.setFormatter(get_console_formatter())
    return handler