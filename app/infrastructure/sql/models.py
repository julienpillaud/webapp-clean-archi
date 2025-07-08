import uuid

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class OrmBase(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)


post_tag = Table(
    "post_tag",
    OrmBase.metadata,
    Column[uuid.UUID](
        "post_id", ForeignKey("post.id", ondelete="CASCADE"), primary_key=True
    ),
    Column[uuid.UUID](
        "tag_id", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True
    ),
)


class OrmUser(OrmBase):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str]
    hashed_password: Mapped[str]

    posts: Mapped[list["OrmPost"]] = relationship(cascade="all, delete-orphan")


class OrmPost(OrmBase):
    __tablename__ = "post"

    title: Mapped[str]
    content: Mapped[str]
    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )

    tags: Mapped[list["OrmTag"]] = relationship(secondary=post_tag)


class OrmTag(OrmBase):
    __tablename__ = "tag"

    name: Mapped[str] = mapped_column(unique=True)
