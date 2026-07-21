# Backing Platform — Mealie

`mealie-mcp` is a **client** of a [Mealie](https://mealie.io/) recipe-manager instance.
This page provides a Docker recipe for deploying one locally to serve as the target of
`MEALIE_BASE_URL`. For production topologies, follow the upstream
[Mealie documentation](https://docs.mealie.io/).

!!! note "Backing-system recipe"
    Each connector in the ecosystem follows the same convention — a
    `docs/platform.md` recipe for the system it integrates with, accompanied by a
    sample Compose stack that mirrors [`services/`](https://github.com/Knuckles-Team).
    Systems offered only as a managed service have no local recipe.

## Single-node deployment (Compose)

Mealie publishes the `ghcr.io/mealie-recipes/mealie` image. The following stack runs one
Mealie instance on `:9000` backed by PostgreSQL:

```yaml
# docker/mealie.compose.yml
services:
  mealie:
    image: ghcr.io/mealie-recipes/mealie:v3.2.0
    container_name: mealie
    hostname: mealie
    restart: unless-stopped
    ports:
      - "9000:9000"
    environment:
      ALLOW_SIGNUP: "true"
      PUID: 1000
      PGID: 1000
      TZ: America/Chicago
      BASE_URL: http://localhost:9000
      DB_ENGINE: postgres
      POSTGRES_USER: mealie
      POSTGRES_PASSWORD: mealie
      POSTGRES_SERVER: postgres
      POSTGRES_PORT: 5432
      POSTGRES_DB: mealie
    volumes:
      - mealie-data:/app/data/
    depends_on:
      - postgres

  postgres:
    image: postgres:17
    container_name: mealie-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: mealie
      POSTGRES_PASSWORD: mealie
      POSTGRES_DB: mealie
    volumes:
      - mealie-pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 30s
      timeout: 20s
      retries: 3

volumes:
  mealie-data:
  mealie-pgdata:
```

```bash
docker compose -f docker/mealie.compose.yml up -d

# Wait for the API to answer
curl -s http://localhost:9000/api/app/about
```

Sign in to the web UI at `http://localhost:9000`, then create an API token under
**Settings → API Tokens** to use as `MEALIE_TOKEN`.

## Connect mealie-mcp

```bash
export MEALIE_BASE_URL=http://localhost:9000
export MEALIE_TOKEN=your_api_token
# export MEALIE_TLS_PROFILE=...          # only needed for self-signed/private-PKI TLS

mealie-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

## Combined deployment

A combined stack places Mealie and the MCP server on one Docker network, so the server
reaches Mealie by container name:

```yaml
# docker/stack.compose.yml
services:
  mealie:
    image: ghcr.io/mealie-recipes/mealie:v3.2.0
    hostname: mealie
    ports: ["9000:9000"]
    environment:
      ALLOW_SIGNUP: "true"
      BASE_URL: http://mealie:9000
    volumes: ["mealie-data:/app/data/"]

  mealie-mcp:
    image: knucklessg1/mealie-mcp:latest
    depends_on: [mealie]
    environment:
      - MEALIE_BASE_URL=http://mealie:9000
      - MEALIE_TOKEN=your_api_token
      - TRANSPORT=streamable-http
      - HOST=0.0.0.0
      - PORT=8000
    ports: ["8000:8000"]

volumes:
  mealie-data:
```

```bash
docker compose -f docker/stack.compose.yml up -d
```
