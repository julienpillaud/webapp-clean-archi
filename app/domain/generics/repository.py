from typing import Protocol

from app.domain.generics.entities import GenericEntity
from app.domain.interfaces.repository import BaseRepositoryProtocol


class GenericEntityRepositoryProtocol(
    BaseRepositoryProtocol[GenericEntity], Protocol
): ...
