import logging
from typing import ClassVar


class ColoredFormatter(logging.Formatter):
    colors: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[34m",  # blue
        "INFO": "\033[36m",  # cyan
        "WARNING": "\033[33m",  # yellow
        "ERROR": "\033[31m",  # red
        "CRITICAL": "\033[35m",  # magenta
    }
    reset = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.colors.get(record.levelname, self.reset)
        message = super().format(record)
        return f"{color}{message}{self.reset}"
