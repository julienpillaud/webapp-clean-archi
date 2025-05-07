from sqlalchemy import select

from app.domain.entities import TagName
from app.domain.exceptions import NotFoundError
from app.domain.posts.entities import Post
from app.domain.users.entities import User
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.repository.base import BaseSqlRepository
from app.infrastructure.repository.models import OrmUser


class UserSqlRepository(
    BaseSqlRepository[User, OrmUser],
    UserRepositoryProtocol,
):
    domain_model = User
    orm_model = OrmUser

    def get_by_email(self, email: str) -> User | None:
        stmt = select(OrmUser).where(OrmUser.email == email)
        orm_entity = self.session.execute(stmt).scalar_one_or_none()
        return self.orm_to_domain_entity(orm_entity=orm_entity) if orm_entity else None

    def update(self, entity: User, /) -> User:
        orm_entity = self._get_entity_by_id(entity_id=entity.id)
        if not orm_entity:
            raise NotFoundError("Entity not found")

        for key, value in entity.model_dump(exclude={"id", "posts"}).items():
            if hasattr(orm_entity, key):
                setattr(orm_entity, key, value)

        self.session.flush()
        return self.orm_to_domain_entity(orm_entity=orm_entity)

    def orm_to_domain_entity(self, orm_entity: OrmUser) -> User:
        return User(
            username=orm_entity.username,
            id=orm_entity.id,
            email=orm_entity.email,
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
