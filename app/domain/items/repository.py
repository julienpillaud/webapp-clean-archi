from enum import StrEnum
from typing import Protocol

from app.domain.interfaces.repository import RepositoryProtocol
from app.domain.items.entities import Item


class RepositoryType(StrEnum):
    RELATIONAL = "relational"
    DOCUMENT = "document"


class ItemRepositoryProtocol(RepositoryProtocol[Item], Protocol): ...
