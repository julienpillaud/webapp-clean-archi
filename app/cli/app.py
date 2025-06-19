import typer

from app.cli.users import app as users_app
from app.domain.domain import Domain


def create_cli_app(domain: Domain) -> typer.Typer:
    app = typer.Typer(no_args_is_help=True)
    app.add_typer(users_app, name="users")

    @app.callback()
    def main(ctx: typer.Context) -> None:
        ctx.obj = {"domain": domain}

    return app
