# Webapp Clean Architecture

## Architecture rules

- The `Domain` class is injected into API routes via FastAPI’s `Depends` mechanism
  to expose all business commands through a single interface.
- API routes should call only one domain command to have only one unit of work per request.
