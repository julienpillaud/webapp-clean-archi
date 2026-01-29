import uuid

from cleanstack.exceptions import NotFoundError

from app.domain.context import ContextProtocol
from app.domain.entities import EntityId, PaginatedResponse, Pagination
from app.domain.filters import FilterEntity
from app.domain.posts.entities import Post, PostCreate, PostUpdate


def create_post_command(context: ContextProtocol, /, data: PostCreate) -> Post:
    author = context.user_repository.get_by_id(data.author_id)
    if not author:
        raise NotFoundError(f"User '{data.author_id}' not found.")

    post = Post(
        id=uuid.uuid7(),
        title=data.title,
        content=data.content,
        author_id=author.id,
        tags=data.tags,
    )
    return context.post_repository.create(post)


def delete_post_command(context: ContextProtocol, /, post_id: EntityId) -> None:
    post = context.post_repository.get_by_id(post_id)
    if not post:
        raise NotFoundError(f"Post '{post_id}' not found.")

    context.post_repository.delete(post)


def get_post_command(context: ContextProtocol, /, post_id: EntityId) -> Post:
    post = context.post_repository.get_by_id(post_id)
    if not post:
        raise NotFoundError(f"Post '{post_id}' not found")

    return post


def get_posts_command(
    context: ContextProtocol,
    /,
    pagination: Pagination | None = None,
    search: str | None = None,
    filters: list[FilterEntity] | None = None,
) -> PaginatedResponse[Post]:
    return context.post_repository.get_all(
        pagination=pagination,
        search=search,
        filters=filters,
    )


def update_post_command(
    context: ContextProtocol, /, post_id: EntityId, data: PostUpdate
) -> Post:
    post = context.post_repository.get_by_id(post_id)
    if not post:
        raise NotFoundError(f"Post '{post_id}' not found")

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(post, key, value)

    return context.post_repository.update(post)
