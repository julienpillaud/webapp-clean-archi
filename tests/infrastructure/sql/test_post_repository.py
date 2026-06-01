import uuid

from cleanstack.entities import DEFAULT_PAGINATION_SIZE
from sqlalchemy.orm import Session

from app.infrastructure.sql.models import OrmPost
from app.infrastructure.sql.posts import PostSQLRepository
from tests.plugins.factories import Factory


def test_get_posts(factory: Factory, post_repository: PostSQLRepository) -> None:
    posts_count = 5
    factory.posts.create_many(posts_count)

    result = post_repository.get_all()

    assert result.total == posts_count
    assert result.size == DEFAULT_PAGINATION_SIZE
    assert len(result.items) == posts_count


def test_get_post(factory: Factory, post_repository: PostSQLRepository) -> None:
    post = factory.posts.create_one()

    result = post_repository.get_by_id(post.id)

    assert result
    assert result.id == post.id
    assert result.title == post.title
    assert result.content == post.content
    assert result.author_id == post.author_id
    assert result.tags
    assert result.tags == post.tags


def test_get_post_not_found(post_repository: PostSQLRepository) -> None:
    result = post_repository.get_by_id(uuid.uuid7())

    assert result is None


def test_save_post(
    factory: Factory,
    post_repository: PostSQLRepository,
    session: Session,
) -> None:
    post = factory.posts.build()

    post_repository.save(post)
    post_repository.session.commit()

    result = session.get(OrmPost, post.id)

    assert result
    assert result.id == post.id
    assert result.title == post.title
    assert result.content == post.content
    assert result.author_id == post.author_id
    assert result.tags
    assert [tag.name for tag in result.tags] == post.tags


def test_update_post(
    factory: Factory,
    post_repository: PostSQLRepository,
    session: Session,
) -> None:
    post = factory.posts.create_one()
    post.title = "Updated title"

    post_repository.update(post)
    post_repository.session.commit()

    result = session.get(OrmPost, post.id)
    assert result
    assert result.id == post.id
    assert result.title == post.title
    assert result.content == post.content
    assert result.author_id == post.author_id
    assert result.tags
    assert [tag.name for tag in result.tags] == post.tags


def test_remove_post(
    factory: Factory,
    post_repository: PostSQLRepository,
    session: Session,
) -> None:
    post = factory.posts.create_one()

    post_repository.remove(post)
    post_repository.session.commit()

    result = session.get(OrmPost, post.id)
    assert result is None
