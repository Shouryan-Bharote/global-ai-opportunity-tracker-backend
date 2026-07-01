from .logger import logger

def get_logger(name: str):
    """Returns a configured logger for the given module name."""
    return logger

__all__ = ["logger", "get_logger"]
