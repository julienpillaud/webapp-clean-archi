import json
import logging.config
from pathlib import Path

from app.cli.app import create_cli_app
from app.core.config import Settings

settings = Settings(_env_file=".env")


if __name__ == "__main__":
    config = json.loads(Path("app/core/logging/config.json").read_text())
    logging.config.dictConfig(config)
    app = create_cli_app(settings=settings)
    app()
