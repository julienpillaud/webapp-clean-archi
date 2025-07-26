from pymongo.collection import Collection

from app.domain.posts.entities import Post
from app.infrastructure.mongo.base import MongoDocument
from factories.mongo import MongoBaseFactory
from factories.posts.base import PostBaseFactory
from factories.users.base import UserBaseFactory


class PostMongoFactory(MongoBaseFactory[Post], PostBaseFactory):
    def __init__(
        self,
        collection: Collection[MongoDocument],
        user_factory: UserBaseFactory,
    ) -> None:
        MongoBaseFactory.__init__(self, collection=collection)
        PostBaseFactory.__init__(self, user_factory=user_factory)
