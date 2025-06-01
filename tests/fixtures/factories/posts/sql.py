from sqlalchemy.orm import Session

from app.domain.posts.entities import Post
from app.infrastructure.sql.models import OrmPost, OrmTag
from tests.fixtures.factories.posts.base import PostBaseFactory
from tests.fixtures.factories.sql import SqlBaseFactory
from tests.fixtures.factories.users.base import UserBaseFactory


class PostSqlFactory(SqlBaseFactory[Post, OrmPost], PostBaseFactory):
    def __init__(self, session: Session, user_factory: UserBaseFactory) -> None:
        SqlBaseFactory.__init__(self, session=session)
        PostBaseFactory.__init__(self, user_factory=user_factory)

    def _to_database_entity(self, entity: Post) -> OrmPost:
        return OrmPost(
            id=entity.id,
            title=entity.title,
            content=entity.content,
            author_id=entity.author_id,
            tags=[OrmTag(name=tag) for tag in entity.tags],
        )
