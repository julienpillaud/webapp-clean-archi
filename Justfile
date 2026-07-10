default:
    just --list

dev:
    docker compose -f compose-dev.yaml up -d

dev-down:
    docker compose -f compose-dev.yaml down

lint:
    uv run ruff check --fix || true
    uv run ruff format
    uv run ty check

tests *options="":
    uv run pytest {{ options }}
