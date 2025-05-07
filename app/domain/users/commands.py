import uuid

from app.domain.context import ContextProtocol
from app.domain.entities import PaginatedResponse, Pagination
from app.domain.exceptions import AlreadyExistsError, NotFoundError
from app.domain.users.entities import User, UserCreate, UserUpdate


def create_user_command(context: ContextProtocol, data: UserCreate) -> User:
    existing_user = context.user_repository.get_by_email(email=data.email)
    if existing_user:
        raise AlreadyExistsError(f"User '{data.email}' already exists.")

    user = User(
        id=uuid.uuid4(),
        username=data.username,
        email=data.email,
        posts=[],
    )
    return context.user_repository.create(user)


def delete_user_command(context: ContextProtocol, user_id: uuid.UUID) -> None:
    user = context.user_repository.get_by_id(user_id)
    if not user:
        raise NotFoundError(f"User '{user_id}' not found")

    context.user_repository.delete(user_id)


def get_user_command(context: ContextProtocol, user_id: uuid.UUID) -> User:
    user = context.user_repository.get_by_id(user_id)
    if not user:
        raise NotFoundError(f"User '{user_id}' not found.")
    return user


def get_users_command(
    context: ContextProtocol, pagination: Pagination
) -> PaginatedResponse[User]:
    return context.user_repository.get_all(pagination=pagination)


def update_user_command(
    context: ContextProtocol, user_id: uuid.UUID, data: UserUpdate
) -> User:
    user = context.user_repository.get_by_id(user_id)
    if not user:
        raise NotFoundError(f"User '{user_id}' not found")

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(user, key, value)

    return context.user_repository.update(user)
