default:
    just --list

init:
    uv sync
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

run:
    uv run uvicorn app.core.app:app --reload --log-config app/core/logging/config.json
