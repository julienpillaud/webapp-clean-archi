from cleanstack.infrastructure.mongodb.uow import MongoDBContext, MongoDBUnitOfWork
from cleanstack.infrastructure.sql.uow import SQLContext, SQLUnitOfWork

from app.core.config import Settings
from app.core.context import Context, context_transaction

settings = Settings()
sql_context = SQLContext.from_settings(url=str(settings.postgres_dsn))
sql_uow = SQLUnitOfWork(context=sql_context)
mongo_context = MongoDBContext.from_settings(
    host=settings.mongo_uri,
    database_name=settings.mongo_database,
)
mongo_uow = MongoDBUnitOfWork(context=mongo_context)
context = Context(
    settings=settings,
    sql_uow=sql_uow,
    mongo_context=mongo_context,
    mongo_uow=mongo_uow,
)


with context_transaction(context=context):
    r = context.item_document_repository.get_all()
    print(r)
    context.mongo_context.database["dev"].insert_one(
        {"name": "test"}, session=mongo_uow.session
    )
