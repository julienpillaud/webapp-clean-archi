from typing import NewType

from cleanstack.entities import DomainModel, EntityId
from pydantic import BaseModel, field_validator

TagName = NewType("TagName", str)


class Post(DomainModel):
    title: str
    content: str
    author_id: EntityId
    tags: list[TagName]


class PostCreate(BaseModel):
    title: str
    content: str
    author_id: EntityId
    tags: list[TagName] = []

    @field_validator("tags", mode="after")
    @classmethod
    def unique(cls, tags: list[TagName]) -> list[TagName]:
        if len(tags) != len(set(tags)):
            raise ValueError("Tag names must be unique")
        return tags


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    tags: list[TagName] | None = None
