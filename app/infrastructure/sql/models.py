import datetime
import uuid

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.sql.entities import OrmEntity

post_tag = Table(
    "post_tag",
    OrmEntity.metadata,
    Column[uuid.UUID](
        "post_id", ForeignKey("post.id", ondelete="CASCADE"), primary_key=True
    ),
    Column[uuid.UUID](
        "tag_id", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True
    ),
)


class OrmUser(OrmEntity):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str]
    hashed_password: Mapped[str]

    posts: Mapped[list[OrmPost]] = relationship(cascade="all, delete-orphan")


class OrmPost(OrmEntity):
    __tablename__ = "post"

    title: Mapped[str]
    content: Mapped[str]
    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )

    tags: Mapped[list[OrmTag]] = relationship(secondary=post_tag)


class OrmTag(OrmEntity):
    __tablename__ = "tag"

    name: Mapped[str] = mapped_column(unique=True)


class OrmDummy(OrmEntity):
    __tablename__ = "dummy"

    uuid_field: Mapped[uuid.UUID]
    string_field: Mapped[str]
    int_field: Mapped[int]
    float_field: Mapped[float]
    bool_field: Mapped[bool]
    date_field: Mapped[datetime.date]
    datetime_field: Mapped[datetime.datetime]
