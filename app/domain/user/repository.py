from app.domain.interfaces.repository import BaseRepositoryProtocol
from app.domain.user.entities import User


class UserRepositoryProtocol(BaseRepositoryProtocol[User]):
    def get_by_email(self, email: str) -> User | None: ...
