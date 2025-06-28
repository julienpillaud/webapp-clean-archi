from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.domain.posts.entities import Post, TagName
from app.domain.users.entities import User
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.sql.base import BaseSqlRepository
from app.infrastructure.sql.models import OrmPost, OrmUser


class UserSqlRepository(BaseSqlRepository[User, OrmUser], UserRepositoryProtocol):
    domain_model = User
    orm_model = OrmUser
    select_options = (selectinload(OrmUser.posts).selectinload(OrmPost.tags),)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(OrmUser).where(OrmUser.email == email)
        orm_entity = self.session.execute(stmt).scalar_one_or_none()

        return self._to_domain_entity(orm_entity=orm_entity) if orm_entity else None

    def update(self, entity: User, /) -> User:
        assert entity.id is not None

        db_entity = self._get_db_entity(entity_id=entity.id)
        if not db_entity:
            raise RuntimeError()

        for key, value in entity.model_dump(exclude={"id", "posts"}).items():
            if hasattr(db_entity, key):
                setattr(db_entity, key, value)

        return self._to_domain_entity(orm_entity=db_entity)

    def _to_domain_entity(self, orm_entity: OrmUser) -> User:
        return User(
            id=orm_entity.id,
            email=orm_entity.email,
            username=orm_entity.username,
            hashed_password=orm_entity.hashed_password,
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
