from app.domain.posts.entities import Post
from app.domain.posts.repository import PostRepositoryProtocol
from app.infrastructure.mongo.base import BaseMongoRepository, MongoDocument


class PostMongoRepository(
    BaseMongoRepository[Post],
    PostRepositoryProtocol,
):
    domain_model = Post
    collection_name = "posts"

    def _to_domain_entity(self, document: MongoDocument, /) -> Post:
        # Override to convert ObjectId 'author_id' to string
        return Post(
            id=str(document["_id"]),
            title=document["title"],
            content=document["content"],
            author_id=str(document["author_id"]),
            tags=document.get("tags", []),
        )
