from bson import ObjectId
from pymongo.collection import Collection

from app.domain.posts.entities import Post
from app.infrastructure.mongo.base import MongoDocument
from tests.fixtures.factories.mongo import MongoBaseFactory
from tests.fixtures.factories.posts.base import PostBaseFactory
from tests.fixtures.factories.users.base import UserBaseFactory


class PostMongoFactory(MongoBaseFactory[Post], PostBaseFactory):
    def __init__(
        self,
        collection: Collection[MongoDocument],
        user_factory: UserBaseFactory,
    ) -> None:
        MongoBaseFactory.__init__(self, collection=collection)
        PostBaseFactory.__init__(self, user_factory=user_factory)

    def _to_database_entity(self, entity: Post, /) -> MongoDocument:
        db_entity = entity.model_dump(exclude={"id"})
        db_entity["author_id"] = ObjectId(str(entity.author_id))
        return db_entity
