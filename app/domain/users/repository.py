from typing import Protocol

from app.domain.interfaces.repository import RepositoryProtocol
from app.domain.users.entities import User


class UserRepositoryProtocol(RepositoryProtocol[User], Protocol): ...
