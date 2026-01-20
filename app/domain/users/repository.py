from app.domain.interfaces.repository import RepositoryProtocol
from app.domain.users.entities import User


class UserRepositoryProtocol(RepositoryProtocol[User]):
    def get_by_email(self, email: str) -> User | None: ...
