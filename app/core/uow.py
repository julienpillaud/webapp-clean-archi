from cleanstack.uow import CompositeUniOfWork

from app.infrastructure.mongo.uow import MongoUnitOfWork
from app.infrastructure.sql.uow import SQLUnitOfWork


class UnitOfWork(CompositeUniOfWork):
    def __init__(self, sql: SQLUnitOfWork, mongo: MongoUnitOfWork) -> None:
        self.sql = sql
        self.mongo = mongo
        super().__init__([self.sql, self.mongo])
