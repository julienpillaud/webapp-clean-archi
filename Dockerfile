FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.6.13 /uv /uvx /bin/

WORKDIR /app

COPY . .

RUN uv sync

CMD ["uv", "run", "fastapi", "dev", "app/core/app.py", "--host", "0.0.0.0"]
