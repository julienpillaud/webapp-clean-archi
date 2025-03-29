import uuid

from app.domain.context import ContextProtocol
from app.domain.entities import PaginatedResponse, Pagination
from app.domain.exceptions import NotFoundError
from app.domain.post.entities import Post, PostCreate, PostUpdate


def create_post_command(context: ContextProtocol, data: PostCreate) -> Post:
    author = context.user_repository.get_by_id(data.author_id)
    if not author:
        raise NotFoundError(f"User '{data.author_id}' not found.")

    post = Post(
        id=uuid.uuid4(),
        title=data.title,
        content=data.content,
        author_id=author.id,
        tags=data.tags,
    )
    context.post_repository.create(post)
    return post


def delete_post_command(context: ContextProtocol, post_id: uuid.UUID) -> None:
    post = context.post_repository.get_by_id(post_id)
    if not post:
        raise NotFoundError(f"Post '{post_id}' not found.")

    context.post_repository.delete(post_id)


def get_post_command(context: ContextProtocol, post_id: uuid.UUID) -> Post:
    post = context.post_repository.get_by_id(post_id)
    if not post:
        raise NotFoundError(f"Post '{post_id}' not found")
    return post


def get_posts_command(
    context: ContextProtocol, pagination: Pagination
) -> PaginatedResponse[Post]:
    return context.post_repository.get_all(pagination=pagination)


def update_post_command(
    context: ContextProtocol, post_id: uuid.UUID, data: PostUpdate
) -> Post:
    post = context.post_repository.get_by_id(post_id)
    if not post:
        raise NotFoundError(f"Post '{post_id}' not found")

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(post, key, value)

    context.post_repository.update(post)

    return post
