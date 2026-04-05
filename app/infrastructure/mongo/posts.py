from cleanstack.infrastructure.mongo import MongoDocument, SyncMongoRepository

from app.domain.posts.entities import Post


class PostMongoRepository(SyncMongoRepository[Post]):
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
