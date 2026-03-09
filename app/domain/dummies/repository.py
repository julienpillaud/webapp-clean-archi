from typing import Protocol

from cleanstack.domain import RepositoryProtocol

from app.domain.dummies.entities import Dummy


class DummyRepositoryProtocol(RepositoryProtocol[Dummy], Protocol): ...
