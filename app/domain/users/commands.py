from app.domain.context import ContextProtocol
from app.domain.entities import EntityId, PaginatedResponse, Pagination
from app.domain.exceptions import AlreadyExistsError, NotFoundError
from app.domain.users.entities import User, UserCreate, UserUpdate


def create_user_command(context: ContextProtocol, data: UserCreate) -> User:
    existing_user = context.user_repository.get_by_email(email=data.email)
    if existing_user:
        raise AlreadyExistsError(f"User '{data.email}' already exists.")

    user = User(
        id=None,
        username=data.username,
        email=data.email,
        posts=[],
    )
    return context.user_repository.create(user)


def delete_user_command(context: ContextProtocol, user_id: EntityId) -> None:
    user = context.user_repository.get_by_id(user_id)
    if not user:
        raise NotFoundError(f"User '{user_id}' not found")

    context.user_repository.delete(user)


def get_user_command(context: ContextProtocol, user_id: EntityId) -> User:
    user = context.user_repository.get_by_id(user_id)
    if not user:
        raise NotFoundError(f"User '{user_id}' not found.")
    return user


def get_users_command(
    context: ContextProtocol, pagination: Pagination, search: str | None = None
) -> PaginatedResponse[User]:
    return context.user_repository.get_all(pagination=pagination, search=search)


def update_user_command(
    context: ContextProtocol, user_id: EntityId, data: UserUpdate
) -> User:
    user = context.user_repository.get_by_id(user_id)
    if not user:
        raise NotFoundError(f"User '{user_id}' not found")

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(user, key, value)

    return context.user_repository.update(user)
