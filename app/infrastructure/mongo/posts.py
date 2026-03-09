from cleanstack.infrastructure.mongo.base import MongoRepository
from cleanstack.infrastructure.mongo.types import MongoDocument

from app.domain.posts.entities import Post
from app.domain.posts.repository import PostRepositoryProtocol


class PostMongoRepository(
    MongoRepository[Post],
    PostRepositoryProtocol,
):
    domain_entity_type = Post
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
