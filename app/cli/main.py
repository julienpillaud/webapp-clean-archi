import json
import logging.config
from pathlib import Path

from app.cli.app import create_cli_app
from app.core.config import Settings
from app.core.context.sql import SqlContext
from app.domain.domain import Domain

settings = Settings(_env_file=".env")
context = SqlContext(settings=settings)
domain = Domain(context=context)


if __name__ == "__main__":
    config = json.loads(Path("app/core/logging/config.json").read_text())
    logging.config.dictConfig(config)
    app = create_cli_app(domain=domain)
    app()
