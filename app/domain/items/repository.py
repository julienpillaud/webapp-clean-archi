from typing import Protocol

from app.domain.interfaces.repository import RepositoryProtocol
from app.domain.items.entities import Item


class ItemRepositoryProtocol(RepositoryProtocol[Item], Protocol): ...
