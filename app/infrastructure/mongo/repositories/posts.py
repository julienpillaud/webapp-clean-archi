from cleanstack.infrastructure.mongodb.types import MongoDocument

from app.domain.posts.entities import Post
from app.domain.posts.repository import PostRepositoryProtocol
from app.infrastructure.mongo.base import MongoRepository


class PostMongoRepository(
    MongoRepository[Post],
    PostRepositoryProtocol,
):
    domain_model = Post
    collection_name = "posts"
    searchable_fields = ("title", "content")

    def _to_domain_entity(self, document: MongoDocument, /) -> Post:
        return Post(
            id=document["_id"],
            title=document["title"],
            content=document["content"],
            author_id=document["author_id"],
            tags=document.get("tags", []),
        )
