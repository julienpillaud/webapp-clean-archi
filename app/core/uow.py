from cleanstack.infrastructure.mongodb.uow import MongoDBUnitOfWork
from cleanstack.infrastructure.sql.uow import SQLUnitOfWork
from cleanstack.uow import CompositeUniOfWork


class UnitOfWork(CompositeUniOfWork):
    def __init__(self, sql: SQLUnitOfWork, mongo: MongoDBUnitOfWork) -> None:
        self.sql = sql
        self.mongo = mongo
        super().__init__([self.sql, self.mongo])
