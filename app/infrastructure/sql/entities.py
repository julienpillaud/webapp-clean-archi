from pydantic import BaseModel, ConfigDict
from sqlalchemy import Select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.domain.entities import EntityId


class OrmEntity(DeclarativeBase):
    id: Mapped[EntityId] = mapped_column(primary_key=True)


class QuerySet[T: OrmEntity](BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    count: Select[tuple[T]]
    data: Select[tuple[T]]
