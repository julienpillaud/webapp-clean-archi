import uuid

import typer
from typer.testing import CliRunner

from factories.users import UserFactory


def test_get_users(cli_app: typer.Typer, cli_runner: CliRunner) -> None:
    # Act
    result = cli_runner.invoke(cli_app, ["users", "get-all"])

    # Assert
    assert result.exit_code == 0
    assert "Users" in result.output
    assert "PaginatedResponse" in result.output


def test_get_user(
    user_factory: UserFactory, cli_app: typer.Typer, cli_runner: CliRunner
) -> None:
    # Arrange
    user = user_factory.create_one()

    # Act
    result = cli_runner.invoke(cli_app, ["users", "get", str(user.id)])

    # Assert
    assert result.exit_code == 0
    assert f"id=UUID('{user.id}')" in result.output


def test_get_user_not_found(cli_app: typer.Typer, cli_runner: CliRunner) -> None:
    # Act
    result = cli_runner.invoke(cli_app, ["users", "get", str(uuid.uuid4())])

    # Assert
    assert result.exit_code == 1
    assert "NotFoundError" in result.output


def test_get_user_invalid_user_id(cli_app: typer.Typer, cli_runner: CliRunner) -> None:
    # Act
    result = cli_runner.invoke(cli_app, ["users", "get", "1"])

    # Assert
    assert result.exit_code == 2  # noqa: PLR2004
    assert "Error" in result.output
    assert "Must be UUID or ObjectId." in result.output


def test_create_user(cli_app: typer.Typer, cli_runner: CliRunner) -> None:
    # Act
    user_data = (
        '{"email": "user@mail.com", "password": "password", "username": "Test User"}'
    )
    result = cli_runner.invoke(cli_app, ["users", "create", user_data])

    # Assert
    assert result.exit_code == 0
    assert "User created" in result.output


def test_create_user_already_exists(
    user_factory: UserFactory, cli_app: typer.Typer, cli_runner: CliRunner
) -> None:
    # Arrange
    user = user_factory.create_one()

    # Act
    data = (
        f'{{"email": "{user.email}", '
        f'"password": "password", '
        f'"username": "{user.username}"}}'
    )
    result = cli_runner.invoke(cli_app, ["users", "create", data])

    # Assert
    assert result.exit_code == 1
    assert "AlreadyExistsError" in result.output


def test_create_user_invalid_data(cli_app: typer.Typer, cli_runner: CliRunner) -> None:
    # Act
    data = '{"username}'
    result = cli_runner.invoke(cli_app, ["users", "create", data])

    # Assert
    assert result.exit_code == 2  # noqa: PLR2004
    assert "Error" in result.output
    assert "Can't parse data to 'UserCreate'" in result.output


def test_update_user(
    user_factory: UserFactory, cli_app: typer.Typer, cli_runner: CliRunner
) -> None:
    # Arrange
    user = user_factory.create_one()

    # Act
    data = '{"username": "User Updated"}'
    result = cli_runner.invoke(cli_app, ["users", "update", str(user.id), data])

    # Assert
    assert result.exit_code == 0
    assert "User updated" in result.output


def test_update_user_not_found(cli_app: typer.Typer, cli_runner: CliRunner) -> None:
    # Act
    data = '{"username": "User Updated"}'
    result = cli_runner.invoke(cli_app, ["users", "update", str(uuid.uuid4()), data])

    # Assert
    assert result.exit_code == 1
    assert "NotFoundError" in result.output


def test_update_user_invalid_data(
    user_factory: UserFactory, cli_app: typer.Typer, cli_runner: CliRunner
) -> None:
    # Arrange
    user = user_factory.create_one()

    # Act
    data = '{"username}'
    result = cli_runner.invoke(cli_app, ["users", "update", str(user.id), data])

    # Assert
    assert result.exit_code == 2  # noqa: PLR2004
    assert "Error" in result.output
    assert "Can't parse data to 'UserUpdate" in result.output


def test_delete_user(
    user_factory: UserFactory, cli_app: typer.Typer, cli_runner: CliRunner
) -> None:
    # Arrange
    user = user_factory.create_one()

    # Act
    result = cli_runner.invoke(cli_app, ["users", "delete", str(user.id)])

    # Assert
    assert result.exit_code == 0
    assert "User deleted" in result.output


def test_delete_user_not_found(cli_app: typer.Typer, cli_runner: CliRunner) -> None:
    # Act
    result = cli_runner.invoke(cli_app, ["users", "delete", str(uuid.uuid4())])

    # Assert
    assert result.exit_code == 1
    assert "NotFoundError" in result.output
