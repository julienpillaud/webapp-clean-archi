from app.domain.users.entities import User
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.mongo.base import BaseMongoRepository


class UserMongoRepository(
    BaseMongoRepository[User],
    UserRepositoryProtocol,
):
    domain_model = User
    collection_name = "users"
