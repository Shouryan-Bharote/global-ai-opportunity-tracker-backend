import colorlog


def get_console_formatter() -> colorlog.ColoredFormatter:
    return colorlog.ColoredFormatter(
        fmt=(
    "%(asctime)s | "
    "%(log_color)s%(levelname)-8s%(reset)s | "
    "%(name)s | "
    "%(module)s:%(lineno)d | "
    "%(message)s"
),
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
        secondary_log_colors={},
        reset=True,
    )