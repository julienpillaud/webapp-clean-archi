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
    app_colors: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[38;5;198m",  # unicorn pink
        "INFO": "\033[38;5;48m",  # bright green
    }
    reset = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.colors.get(record.levelname, self.reset)
        if record.name.startswith("app.") and record.levelname in self.app_colors:
            color = self.app_colors[record.levelname]

        message = super().format(record)
        return f"{color}{message}{self.reset}"
