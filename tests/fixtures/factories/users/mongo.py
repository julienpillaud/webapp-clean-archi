from pymongo.collection import Collection

from app.domain.users.entities import User
from app.infrastructure.mongo.base import MongoDocument
from tests.fixtures.factories.mongo import MongoBaseFactory
from tests.fixtures.factories.users.base import UserBaseFactory


class UserMongoFactory(MongoBaseFactory[User], UserBaseFactory):
    def __init__(self, collection: Collection[MongoDocument]) -> None:
        MongoBaseFactory.__init__(self, collection=collection)
        UserBaseFactory.__init__(self)

    def _to_database_entity(self, entity: User, /) -> MongoDocument:
        return entity.model_dump(exclude={"id", "posts"})
