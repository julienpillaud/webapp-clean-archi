import uuid
from typing import Any

from faker import Faker

from app.domain.items.entities import Item
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.mongo.repositories.items import ItemMongoRepository
from app.infrastructure.sql.repositories.items import ItemSQLRepository
from tests.factories.base import BaseMongoFactory, BaseSQLFactory


def generate_item(faker: Faker, **kwargs: Any) -> Item:
    return Item(
        id=uuid.uuid7(),
        name=kwargs["name"] if "name" in kwargs else faker.name(),
    )


class ItemSQLFactory(BaseSQLFactory[Item]):
    def build(self, **kwargs: Any) -> Item:
        return generate_item(faker=self.faker, **kwargs)

    @property
    def repository(self) -> ItemRepositoryProtocol:
        return ItemSQLRepository(session=self.session)


class ItemMongoFactory(BaseMongoFactory[Item]):
    def build(self, **kwargs: Any) -> Item:
        return generate_item(faker=self.faker, **kwargs)

    @property
    def repository(self) -> ItemRepositoryProtocol:
        return ItemMongoRepository(database=self.database)
