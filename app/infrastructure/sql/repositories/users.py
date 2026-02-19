from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.domain.posts.entities import Post, TagName
from app.domain.users.entities import User
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.sql.base import SQLRepository
from app.infrastructure.sql.models import OrmPost, OrmUser


class UserSQLRepository(SQLRepository[User, OrmUser], UserRepositoryProtocol):
    domain_model = User
    orm_model = OrmUser
    select_options = (selectinload(OrmUser.posts).selectinload(OrmPost.tags),)

    def get_by_provider_id(self, provider_id: str, /) -> User | None:
        stmt = select(OrmUser).where(OrmUser.provider_id == provider_id)
        orm_entity = self.session.execute(stmt).scalar_one_or_none()
        return self._to_domain_entity(orm_entity=orm_entity) if orm_entity else None

    def _to_domain_entity(self, orm_entity: OrmUser) -> User:
        return User(
            id=orm_entity.id,
            provider_id=orm_entity.provider_id,
            email=orm_entity.email,
            username=orm_entity.username,
            posts=[
                Post(
                    id=post.id,
                    title=post.title,
                    content=post.content,
                    author_id=post.author_id,
                    tags=[TagName(tag.name) for tag in post.tags],
                )
                for post in orm_entity.posts
            ],
        )
