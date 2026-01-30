from typing import Protocol

from app.domain.dummies.entities import Dummy
from app.domain.interfaces.repository import RepositoryProtocol


class DummyRepositoryProtocol(RepositoryProtocol[Dummy], Protocol): ...
