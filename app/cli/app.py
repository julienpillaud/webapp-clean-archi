import typer

from app.cli.posts import app as posts_app
from app.cli.users import app as users_app
from app.core.config import Settings
from app.core.context import Context
from app.core.uow import UnitOfWork
from app.domain.domain import Domain
from app.infrastructure.mongo.uow import MongoContext, MongoUnitOfWork
from app.infrastructure.sql.uow import SQLContext, SQLUnitOfWork


def create_cli_app(settings: Settings) -> typer.Typer:
    app = typer.Typer(no_args_is_help=True)
    app.add_typer(users_app, name="users")
    app.add_typer(posts_app, name="posts")

    @app.callback()
    def main(ctx: typer.Context) -> None:
        sql_context = SQLContext.from_settings(dsn=str(settings.postgres_dsn))
        sql_uow = SQLUnitOfWork(context=sql_context)

        mongo_context = MongoContext.from_settings(
            uri=settings.mongo_uri,
            database_name=settings.mongo_database,
        )
        mongo_uow = MongoUnitOfWork(context=mongo_context)

        uow = UnitOfWork(sql=sql_uow, mongo=mongo_uow)
        context = Context(settings=settings, uow=uow)
        domain = Domain(uow=uow, context=context)

        ctx.obj = {"domain": domain}

    return app
