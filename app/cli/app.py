import typer

from app.cli.posts import app as posts_app
from app.cli.users import app as users_app
from app.domain.domain import Domain


def create_cli_app(domain: Domain) -> typer.Typer:
    # Passes the callback directly to Typer to avoid runtime @app.callback() decorator cost
    app = typer.Typer(no_args_is_help=True, callback=_cli_callback_factory(domain))
    app.add_typer(users_app, name="users")
    app.add_typer(posts_app, name="posts")
    return app


def _cli_callback_factory(domain: Domain):
    # Returns a callback function with bound domain to avoid closure cost per-app creation
    def main(ctx: typer.Context) -> None:
        ctx.obj = {"domain": domain}

    return main
