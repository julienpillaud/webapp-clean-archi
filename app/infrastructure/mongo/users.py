from app.domain.posts.entities import Post
from app.domain.users.entities import User
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.mongo.base import BaseMongoRepository, MongoDocument


class UserMongoRepository(BaseMongoRepository[User], UserRepositoryProtocol):
    domain_model = User
    collection_name = "users"

    def get_by_email(self, email: str) -> User | None:
        user = self.collection.find_one({"email": email})
        return self._to_domain_entity(user) if user else None

    def _to_domain_entity(self, document: MongoDocument, /) -> User:
        return User(
            id=document["_id"],
            email=document["email"],
            username=document["username"],
            hashed_password=document["hashed_password"],
            posts=[
                Post(
                    id=post["_id"],
                    title=post["title"],
                    content=post["content"],
                    author_id=post["author_id"],
                    tags=post.get("tags", []),
                )
                for post in document.get("posts", [])
            ],
        )

    @staticmethod
    def _to_database_entity(entity: User, /) -> MongoDocument:
        document = entity.model_dump(exclude={"id", "posts"})
        document["_id"] = entity.id
        return document

    @staticmethod
    def _aggregation_pipeline() -> list[MongoDocument]:
        return [
            {
                "$lookup": {
                    "from": "posts",
                    "localField": "_id",
                    "foreignField": "author_id",
                    "as": "posts",
                }
            }
        ]
