import logging
from typing import ClassVar

MAX_NAME_LENGTH = 35
LOG_FORMAT = f"%(asctime)s [%(levelname)8s] %(name){MAX_NAME_LENGTH}s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
PROJECT_LOGGER_NAME = "app"


class ColoredFormatter(logging.Formatter):
    colors_mapping: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[34m",  # blue
        "INFO": "\033[36m",  # cyan
        "WARNING": "\033[33m",  # yellow
        "ERROR": "\033[31m",  # red
        "CRITICAL": "\033[35m",  # magenta
    }
    app_colors_mapping: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[38;5;198m",  # unicorn pink
        "INFO": "\033[38;5;48m",  # bright green
    }
    reset_color = "\033[0m"

    def __init__(self) -> None:
        super().__init__(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        color = self._get_color(record)
        self._strip_record_name(record)
        message = super().format(record)
        return f"{color}{message}{self.reset_color}"

    def _get_color(self, record: logging.LogRecord) -> str:
        color = self.colors_mapping.get(record.levelname, self.reset_color)
        if (
            record.name.startswith(PROJECT_LOGGER_NAME)
            and record.levelname in self.app_colors_mapping
        ):
            color = self.app_colors_mapping[record.levelname]
        return color

    @staticmethod
    def _strip_record_name(record: logging.LogRecord) -> None:
        if len(record.name) > MAX_NAME_LENGTH:
            record.name = f"...{record.name[-(MAX_NAME_LENGTH - 3) :]}"
