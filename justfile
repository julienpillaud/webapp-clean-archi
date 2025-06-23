default:
    just --list

# Run the application
init:
    uv sync --all-extras
    uv run pre-commit install

db-postgres container_name port env_file:
	docker run -d \
	--name {{container_name}} \
	-p {{port}}:5432 \
	--env-file {{env_file}} \
	--restart unless-stopped \
	postgres:17

postgres-dev port="5433" env_file=".env":
    just db-postgres webapp-clean-archi-dev {{port}} {{env_file}}

postgres-test port="5432" env_file=".env.test":
    just db-postgres webapp-clean-archi-test {{port}} {{env_file}}

migrate:
    uv run alembic upgrade head

run port="8000":
    uv run uvicorn app.core.app:app \
    --port {{port}} \
    --reload \
    --log-config app/core/logging/config.json

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
