import typer

from app.cli.posts import app as posts_app
from app.cli.users import app as users_app
from app.core.config import Settings
from app.core.context import Context
from app.core.uow import UnitOfWork
from app.domain.domain import Domain
from app.infrastructure.mongo.uow import MongoUnitOfWork
from app.infrastructure.sql.uow import SQLUnitOfWork


def create_cli_app(settings: Settings) -> typer.Typer:
    app = typer.Typer(no_args_is_help=True)
    app.add_typer(users_app, name="users")
    app.add_typer(posts_app, name="posts")

    @app.callback()
    def main(ctx: typer.Context) -> None:
        sql_uow = SQLUnitOfWork(settings=settings)
        mongo_uow = MongoUnitOfWork(settings=settings)
        uow = UnitOfWork(sql=sql_uow, mongo=mongo_uow)
        context = Context(settings=settings, uow=uow)
        domain = Domain(uow=uow, context=context)

        ctx.obj = {"domain": domain}

    return app
