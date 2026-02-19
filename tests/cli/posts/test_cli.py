import uuid

import typer
from typer.testing import CliRunner

from tests.factories.posts import PostSQLFactory
from tests.factories.users import UserSQLFactory


def test_get_posts(cli_app: typer.Typer, cli_runner: CliRunner) -> None:
    # Act
    result = cli_runner.invoke(cli_app, ["posts", "get-all"])

    # Assert
    assert result.exit_code == 0
    assert "Posts" in result.output
    assert "PaginatedResponse" in result.output


def test_get_post(
    post_factory: PostSQLFactory, cli_app: typer.Typer, cli_runner: CliRunner
) -> None:
    # Arrange
    post = post_factory.create_one()

    # Act
    result = cli_runner.invoke(cli_app, ["posts", "get", str(post.id)])

    # Assert
    assert result.exit_code == 0
    assert f"id=UUID('{post.id}')" in result.output


def test_get_post_not_found(cli_app: typer.Typer, cli_runner: CliRunner) -> None:
    # Act
    result = cli_runner.invoke(cli_app, ["posts", "get", str(uuid.uuid4())])

    # Assert
    assert result.exit_code == 1
    assert "NotFoundError" in result.output


def test_get_post_invalid_id(cli_app: typer.Typer, cli_runner: CliRunner) -> None:
    # Act
    result = cli_runner.invoke(cli_app, ["posts", "get", "1"])

    # Assert
    assert result.exit_code == 2  # noqa: PLR2004
    assert "Error" in result.output
    assert "Must be UUID or ObjectId." in result.output


def test_create_post(
    user_factory: UserSQLFactory,
    cli_app: typer.Typer,
    cli_runner: CliRunner,
) -> None:
    # Arrange
    user = user_factory.create_one()

    # Act
    data = (
        f'{{"title": "New Post", "content": "Some content", "author_id": "{user.id}"}}'
    )
    result = cli_runner.invoke(cli_app, ["posts", "create", data])

    # Assert
    assert result.exit_code == 0
    assert "Post created" in result.output


def test_create_post_invalid_data(cli_app: typer.Typer, cli_runner: CliRunner) -> None:
    # Act
    data = '{"title":'
    result = cli_runner.invoke(cli_app, ["posts", "create", data])

    # Assert
    assert result.exit_code == 2  # noqa: PLR2004
    assert "Error" in result.output
    assert "Can't parse data to 'PostCreate'" in result.output


def test_update_post(
    post_factory: PostSQLFactory, cli_app: typer.Typer, cli_runner: CliRunner
) -> None:
    # Arrange
    post = post_factory.create_one()

    # Act
    data = '{"title": "Updated Title"}'
    result = cli_runner.invoke(cli_app, ["posts", "update", str(post.id), data])

    # Assert
    assert result.exit_code == 0
    assert "Post updated" in result.output


def test_update_post_not_found(cli_app: typer.Typer, cli_runner: CliRunner) -> None:
    # Act
    data = '{"title": "Update"}'
    result = cli_runner.invoke(cli_app, ["posts", "update", str(uuid.uuid4()), data])

    # Assert
    assert result.exit_code == 1
    assert "NotFoundError" in result.output


def test_update_post_invalid_data(
    post_factory: PostSQLFactory, cli_app: typer.Typer, cli_runner: CliRunner
) -> None:
    # Arrange
    post = post_factory.create_one()

    # Act
    data = '{"title":'
    result = cli_runner.invoke(cli_app, ["posts", "update", str(post.id), data])

    # Assert
    assert result.exit_code == 2  # noqa: PLR2004
    assert "Error" in result.output
    assert "Can't parse data to 'PostUpdate'" in result.output


def test_delete_post(
    post_factory: PostSQLFactory, cli_app: typer.Typer, cli_runner: CliRunner
) -> None:
    # Arrange
    post = post_factory.create_one()

    # Act
    result = cli_runner.invoke(cli_app, ["posts", "delete", str(post.id)])

    # Assert
    assert result.exit_code == 0
    assert "Post deleted" in result.output


def test_delete_post_not_found(cli_app: typer.Typer, cli_runner: CliRunner) -> None:
    # Act
    result = cli_runner.invoke(cli_app, ["posts", "delete", str(uuid.uuid4())])

    # Assert
    assert result.exit_code == 1
    assert "NotFoundError" in result.output
