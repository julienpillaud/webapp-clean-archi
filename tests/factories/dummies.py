import uuid
from typing import Any

from faker import Faker

from app.domain.dummies.entities import Dummy
from app.infrastructure.sql.dummies import DummySqlRepository
from app.infrastructure.sql.models import OrmDummy
from tests.factories.base import BaseSqlFactory


def generate_dummy(faker: Faker, **kwargs: Any) -> Dummy:
    return Dummy(
        id=uuid.uuid7(),
        uuid_field=kwargs["uuid_field"] if "uuid_field" in kwargs else uuid.uuid7(),
        string_field=kwargs["string_field"]
        if "string_field" in kwargs
        else faker.name(),
        int_field=kwargs["int_field"] if "int_field" in kwargs else faker.pyint(),
        float_field=kwargs["float_field"]
        if "float_field" in kwargs
        else faker.pyfloat(),
        bool_field=kwargs["bool_field"] if "bool_field" in kwargs else faker.pybool(),
        date_field=kwargs["date_field"]
        if "date_field" in kwargs
        else faker.date_object(),
        datetime_field=kwargs["datetime_field"]
        if "datetime_field" in kwargs
        else faker.date_time(),
    )


class DummyFactory(BaseSqlFactory[Dummy, OrmDummy]):
    repository_class = DummySqlRepository

    def build(self, **kwargs: Any) -> Dummy:
        return generate_dummy(faker=self.faker, **kwargs)
