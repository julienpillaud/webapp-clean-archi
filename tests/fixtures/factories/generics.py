# from typing import Any
#
# from app.domain.generics.entities import GenericEntity
# from tests.fixtures.factories.mongo import MongoBaseFactory
#
#
# class GenericEntityMongoFactory(MongoBaseFactory[GenericEntity]):
#     def _build_entity(self, **kwargs: Any) -> GenericEntity:
#         return GenericEntity(id=None, name=kwargs.get("name", self.faker.name()))
