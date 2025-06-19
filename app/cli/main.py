import json
import logging.config
from pathlib import Path

import typer

from app.cli.users import app as users_app
from app.core.config import Settings
from app.core.context.sql import SqlContext
from app.domain.domain import Domain

settings = Settings(_env_file=".env")
SqlContext.initialize(settings=settings)
context = SqlContext()
domain = Domain(context=context)

app = typer.Typer(no_args_is_help=True)
app.add_typer(users_app, name="users")


@app.callback()
def main(ctx: typer.Context) -> None:
    ctx.obj = {"domain": domain}


if __name__ == "__main__":
    config = json.loads(Path("app/core/logging/config.json").read_text())
    logging.config.dictConfig(config)
    app()
