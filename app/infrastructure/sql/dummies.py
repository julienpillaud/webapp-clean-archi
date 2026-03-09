from cleanstack.infrastructure.sql.base import SQLRepository

from app.domain.dummies.entities import Dummy
from app.domain.dummies.repository import DummyRepositoryProtocol
from app.infrastructure.sql.models import OrmDummy


class DummySQLRepository(SQLRepository[Dummy, OrmDummy], DummyRepositoryProtocol):
    domain_entity_type = Dummy
    orm_model_type = OrmDummy
