import 'scripts/container.just'

default:
    just --list

# Run the application
init:
    uv sync --all-extras
    uv run pre-commit install

run-app port="8000":
    uv run uvicorn app.core.app:app \
    --port {{ port }} \
    --reload --reload-dir app \
    --log-config app/core/logging/config.json

# Development tools
lint:
    uv run pre-commit run --all-files

tests *options="--log-cli-level=INFO":
    uv run pytest {{ options }}

# Command line interface
cli *options="":
    uv run python -m app.cli.main {{ options }}

dev:
    docker compose up -d

dev-down:
    docker compose down
