.PHONY: help init db-dev db-test pre-commit tests coverage lint

help:
	@echo "Available commands:"
	@echo "  init       - Install dependencies and pre-commit hooks"
	@echo "  pre-commit - Run pre-commit hooks on all files"
	@echo "  tests      - Run tests"
	@echo "  coverage   - Run tests with coverage"
	@echo "  lint       - Format and check code"

init:
	uv sync
	uv run pre-commit install

db-dev:
	set -a && source .env && set +a && \
	docker run -d \
	--name $$POSTGRES_CONTAINER_NAME \
	-p $$POSTGRES_PORT:5432 \
	--env-file .env \
	--restart unless-stopped \
	postgres:17

db-test:
	set -a && source .env.test && set +a && \
	docker run -d \
	--name $$POSTGRES_CONTAINER_NAME \
	-p $$POSTGRES_PORT:5432 \
	--env-file .env.test \
	--restart unless-stopped \
	postgres:17

pre-commit:
	uv run pre-commit run --all-files

tests:
	uv run pytest

coverage:
	uv run coverage run --source=app -m pytest
	uv run coverage report --show-missing
	uv run coverage html

lint:
	uv run ruff format
	uv run ruff check --fix || true
	uv run mypy .
