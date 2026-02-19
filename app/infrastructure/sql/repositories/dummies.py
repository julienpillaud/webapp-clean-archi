from typing import Any, ClassVar

from sqlalchemy.orm import InstrumentedAttribute

from app.domain.dummies.entities import Dummy
from app.domain.dummies.repository import DummyRepositoryProtocol
from app.infrastructure.sql.base import SQLRepository
from app.infrastructure.sql.models import OrmDummy


class DummySQLRepository(SQLRepository[Dummy, OrmDummy], DummyRepositoryProtocol):
    domain_model = Dummy
    orm_model = OrmDummy
    filterable_fields: ClassVar[dict[str, InstrumentedAttribute[Any]]] = {
        "uuid_field": OrmDummy.uuid_field,
        "string_field": OrmDummy.string_field,
        "int_field": OrmDummy.int_field,
        "float_field": OrmDummy.float_field,
        "bool_field": OrmDummy.bool_field,
        "date_field": OrmDummy.date_field,
        "datetime_field": OrmDummy.datetime_field,
    }
