import typer
from cleanstack.infrastructure.mongodb.uow import MongoDBContext, MongoDBUnitOfWork
from cleanstack.infrastructure.sql.uow import SQLContext, SQLUnitOfWork

from app.cli.posts import app as posts_app
from app.cli.users import app as users_app
from app.core.config import Settings
from app.core.context import Context
from app.core.uow import UnitOfWork
from app.domain.domain import Domain


def create_cli_app(settings: Settings) -> typer.Typer:
    app = typer.Typer(no_args_is_help=True)
    app.add_typer(users_app, name="users")
    app.add_typer(posts_app, name="posts")

    @app.callback()
    def main(ctx: typer.Context) -> None:
        sql_context = SQLContext.from_settings(url=str(settings.postgres_dsn))
        sql_uow = SQLUnitOfWork(context=sql_context)

        mongo_context = MongoDBContext.from_settings(
            host=settings.mongo_uri,
            database_name=settings.mongo_database,
        )
        mongo_uow = MongoDBUnitOfWork(context=mongo_context)

        uow = UnitOfWork(sql=sql_uow, mongo=mongo_uow)
        context = Context(
            settings=settings,
            sql_uow=sql_uow,
            mongo_context=mongo_context,
            mongo_uow=mongo_uow,
        )
        domain = Domain(uow=uow, context=context)

        ctx.obj = {"domain": domain}

    return app
