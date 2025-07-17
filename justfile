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
	postgres:latest

postgres-dev port="5433" env_file=".env":
    just db-postgres webapp-postgres-dev {{port}} {{env_file}}

postgres-test port="5432" env_file=".env.test":
    just db-postgres webapp-postgres-test {{port}} {{env_file}}

db-mongo container_name port env_file:
	docker run -d \
	--name {{container_name}} \
	-p {{port}}:27017 \
	--env-file {{env_file}} \
	--restart unless-stopped \
	mongo:latest

mongo-dev port="27018" env_file=".env":
	just db-mongo webapp-mongo-dev {{port}} {{env_file}}

mongo-test port="27017" env_file=".env.test":
	just db-mongo webapp-mongo-test {{port}} {{env_file}}

migrate:
    uv run alembic upgrade head

rabbitmq port="5672" env_file=".env":
    docker run -d \
    --name rabbitmq \
    -p {{port}}:5672 \
    -p 15672:15672 \
    --env-file {{env_file}} \
    --restart unless-stopped \
    rabbitmq:4-management

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
