from cleanstack import EntityId, FilterEntity, PaginatedResponse, Pagination, SortEntity
from cleanstack.sql import SyncSQLRepository
from sqlalchemy.orm import Session

from app.domain.posts.entities import Post, TagName
from app.domain.users.entities import User
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.sql.models import OrmPost, OrmUser


class UserSQLAdapter(SyncSQLRepository[User, OrmUser]):
    def to_domain_entity(self, orm_entity: OrmUser) -> User:
        return User(
            id=orm_entity.id,
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

    def to_database_entity(self, entity: User) -> OrmUser:
        return OrmUser(
            id=entity.id,
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


class UserSQLRepository(UserRepositoryProtocol):
    domain_entity_type = User
    orm_model_type = OrmUser
    searchable_fields = ()

    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = SyncSQLRepository[User, OrmUser].from_binding(
            binding=self,
            session=session,
        )

    def get_all(
        self,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        sort: list[SortEntity] | None = None,
        pagination: Pagination | None = None,
    ) -> PaginatedResponse[User]:
        return self.repository.get_all()

    def get_by_id(self, entity_id: EntityId, /) -> User | None:
        return self.repository.get_by_id(entity_id)

    def save(self, entity: User, /) -> None:
        self.repository.save(entity)
