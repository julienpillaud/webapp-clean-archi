from app.domain.posts.entities import Post
from app.domain.posts.repository import PostRepositoryProtocol
from app.infrastructure.mongo.base import BaseMongoRepository


class PostMongoRepository(
    BaseMongoRepository[Post],
    PostRepositoryProtocol,
):
    domain_model = Post
    collection_name = "posts"
