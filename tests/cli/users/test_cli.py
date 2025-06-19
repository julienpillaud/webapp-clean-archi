import typer
from typer.testing import CliRunner

from app.domain.entities import EntityId
from tests.fixtures.factories.posts.base import PostBaseFactory
from tests.fixtures.factories.users.base import UserBaseFactory


def test_get_users(cli_app: typer.Typer, cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(cli_app, ["users", "get-all"])
    assert result.exit_code == 0
    assert "Users" in result.output
    assert "PaginatedResponse" in result.output


def test_get_user(
    user_factory: UserBaseFactory,
    post_factory: PostBaseFactory,
    cli_app: typer.Typer,
    cli_runner: CliRunner,
) -> None:
    user = user_factory.create_one()
    post_factory.create_many(3, author_id=user.id)

    result = cli_runner.invoke(cli_app, ["users", "get", str(user.id)])
    assert result.exit_code == 0
    assert f"id=UUID('{user.id}')" in result.output


def test_get_user_not_found(
    fake_entity_id: EntityId,
    cli_app: typer.Typer,
    cli_runner: CliRunner,
) -> None:
    result = cli_runner.invoke(cli_app, ["users", "get", str(fake_entity_id)])
    assert result.exit_code == 1
    assert "NotFoundError" in result.output


def test_create_user(cli_app: typer.Typer, cli_runner: CliRunner) -> None:
    user_data = '{"username": "Test User", "email": "user@mail.com"}'
    result = cli_runner.invoke(cli_app, ["users", "create", user_data])
    assert result.exit_code == 0
    assert "User created" in result.output


def test_create_user_already_exists(
    user_factory: UserBaseFactory,
    cli_app: typer.Typer,
    cli_runner: CliRunner,
) -> None:
    user = user_factory.create_one()

    user_data = f'{{"username": "{user.username}", "email": "{user.email}"}}'
    result = cli_runner.invoke(cli_app, ["users", "create", user_data])
    assert result.exit_code == 1
    assert "AlreadyExistsError" in result.output
