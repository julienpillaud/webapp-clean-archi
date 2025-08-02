import 'scripts/container.just'

default:
    just --list

# Run the application
init:
    uv sync --all-extras
    uv run pre-commit install

migrate:
    uv run alembic upgrade head

run-app port="8000":
    uv run uvicorn app.core.app:app \
    --port {{port}} \
    --reload --reload-dir app \
    --log-config app/core/logging/config.json

# Development tools
lint:
    uv run pre-commit run --all-files

tests *options="--log-cli-level=INFO":
    uv run pytest {{options}}

coverage source="app":
	uv run coverage run --source={{source}} -m pytest
	uv run coverage report --show-missing
	uv run coverage html

# Command line interface
cli *options="":
    uv run python -m app.cli.main {{options}}
