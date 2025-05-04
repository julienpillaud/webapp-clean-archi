import uuid
from typing import Any, Generic, TypeVar

import pytest
from faker import Faker
from sqlalchemy.orm import Session

from app.domain.entities import DomainModel, TagName
from app.domain.posts.entities import Post
from app.domain.users.entities import User
from app.infrastructure.repository.models import OrmPost, OrmTag, OrmUser

T = TypeVar("T", bound=DomainModel)
P = TypeVar("P")


class BaseFactory(Generic[T, P]):
    def __init__(self):
        self.faker = Faker()

    def create_one(self, **kwargs: Any) -> T:
        entity = self._build_entity(**kwargs)
        self._insert([entity])
        return entity

    def create_many(self, count: int, /, **kwargs: Any) -> list[T]:
        entities = [self._build_entity(**kwargs) for _ in range(count)]
        self._insert(entities)
        return entities

    def _build_entity(self, **kwargs: Any) -> T:
        """Build a domain entity with the given kwargs."""
        ...

    def _insert(self, entities: list[T]) -> None:
        """Insert the entities into the database."""
        ...

    def _to_database_entity(self, entity: T) -> P:
        """Convert the domain entity to a database-compatible format."""
        ...


class SqlBaseFactory(BaseFactory[T, P]):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def _insert(self, entities: list[T]) -> None:
        db_entities = [self._to_database_entity(entity) for entity in entities]
        self.session.add_all(db_entities)
        self.session.commit()


class UserFactory(SqlBaseFactory[User, OrmUser]):
    def _build_entity(self, **kwargs: Any) -> User:
        return User(
            id=uuid.uuid4(),
            username=kwargs.get("username", self.faker.user_name()),
            email=kwargs.get("email", self.faker.unique.email()),
            posts=[],
        )

    def _to_database_entity(self, entity: User) -> OrmUser:
        return OrmUser(
            id=entity.id,
            username=entity.username,
            email=entity.email,
        )


class PostFactory(SqlBaseFactory[Post, OrmPost]):
    def __init__(self, session: Session, user_factory: UserFactory):
        super().__init__(session)
        self.user_factory = user_factory

    def _build_entity(self, **kwargs: Any) -> Post:
        if not (author_id := kwargs.get("author_id")):
            author_id = self.user_factory.create_one().id

        if not (tags := kwargs.get("tags")):
            num_tags = self.faker.random_int(min=1, max=3)
            tags = [
                TagName(f"{self.faker.unique.lexify(text='?????')}{i}")
                for i in range(num_tags)
            ]

        return Post(
            id=uuid.uuid4(),
            title=kwargs.get("title", self.faker.sentence()),
            content=kwargs.get("content", self.faker.text()),
            author_id=author_id,
            tags=tags,
        )

    def _to_database_entity(self, entity: Post) -> OrmPost:
        return OrmPost(
            id=entity.id,
            title=entity.title,
            content=entity.content,
            author_id=entity.author_id,
            tags=[OrmTag(name=tag) for tag in entity.tags],
        )


@pytest.fixture
def faker() -> Faker:
    return Faker()


@pytest.fixture
def user_factory(session: Session) -> UserFactory:
    return UserFactory(session=session)


@pytest.fixture
def post_factory(session: Session, user_factory: UserFactory) -> PostFactory:
    return PostFactory(session=session, user_factory=user_factory)
