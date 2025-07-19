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
    --reload \
    --log-config app/core/logging/config.json

run-worker:
    uv run watchmedo auto-restart \
    --patterns="*.py" \
    --recursive \
    --directory="." \
    -- celery -A app.core.worker worker --pool=solo --loglevel=info

# Development tools
pre-commit:
	uv run pre-commit run --all-files

lint:
	uv run ruff format
	uv run ruff check --fix || true
	uv run mypy .

tests *options="":
    uv run pytest {{options}}

coverage source="app":
	uv run coverage run --source={{source}} -m pytest
	uv run coverage report --show-missing
	uv run coverage html

# Command line interface
cli *options="":
    uv run python -m app.cli.main {{options}}
