import typer
from typer.testing import CliRunner


def test_get_users(cli_app: typer.Typer, cli_runner: CliRunner) -> None:
    # Act
    result = cli_runner.invoke(cli_app, ["users", "get-all"])

    # Assert
    assert result.exit_code == 0
    assert "Users" in result.output
    assert "PaginatedResponse" in result.output
