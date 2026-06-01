from cleanstack.infrastructure.sql.synchronous.repository import SyncSQLRepository
from sqlalchemy import select

from app.domain.posts.entities import Post, TagName
from app.domain.users.entities import User
from app.infrastructure.sql.models import OrmPost, OrmUser


class UserSQLRepository(SyncSQLRepository[User, OrmUser]):
    domain_entity_type = User
    orm_model_type = OrmUser

    def get_by_provider_id(self, provider_id: str, /) -> User | None:
        stmt = select(OrmUser).where(OrmUser.provider_id == provider_id)
        orm_entity = self.session.execute(stmt).scalar_one_or_none()
        return self.to_domain_entity(orm_entity=orm_entity) if orm_entity else None

    def to_orm_entity(self, entity: User) -> OrmUser:
        return OrmUser(
            id=entity.id,
            provider_id=entity.provider_id,
            email=entity.email,
            username=entity.username,
            posts=[
                OrmPost(
                    id=post.id,
                    title=post.title,
                    content=post.content,
                )
                for post in entity.posts
            ],
        )

    def to_domain_entity(self, orm_entity: OrmUser) -> User:
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
