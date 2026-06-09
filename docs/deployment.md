# Deployment

This page covers running `mealie-mcp` as a long-lived server: the transports, the
optional A2A agent server, a Docker Compose stack, putting it behind a Caddy reverse
proxy, and giving it a DNS name with Technitium. To provision the **Mealie platform**
it connects to, see [Backing Platform](platform.md).

> `mealie-mcp` ships an **MCP server** (console script `mealie-mcp`) and an **A2A
> graph agent** (console script `mealie-agent`). The MCP server is the typed,
> deterministic tool surface; the agent wraps it as a confidence-gated graph router.

## Run the MCP server

The transport is selected with `--transport` (or the `TRANSPORT` env var):

=== "stdio (default)"

    ```bash
    mealie-mcp
    ```
    For IDE / desktop MCP clients that launch the server as a subprocess.

=== "streamable-http"

    ```bash
    mealie-mcp --transport streamable-http --host 0.0.0.0 --port 8000
    ```
    A network server with a `/health` endpoint and `/mcp` route.

=== "sse"

    ```bash
    mealie-mcp --transport sse --host 0.0.0.0 --port 8000
    ```

Health check (HTTP transports):

```bash
curl -s http://localhost:8000/health        # {"status":"OK"}
```

## Configuration (environment)

`mealie-mcp` is configured entirely from the environment. The **required** set:

| Var | Default | Meaning |
|---|---|---|
| `MEALIE_BASE_URL` | — | Mealie instance base URL (required) |
| `MEALIE_TOKEN` | — | Mealie API token (Bearer) |
| `MEALIE_SSL_VERIFY` | `False` | Verify TLS (self-signed homelab) |
| `HOST` | `0.0.0.0` | Bind address (HTTP transports) |
| `PORT` | `8000` | Bind port (HTTP transports) |
| `TRANSPORT` | `stdio` | `stdio`, `streamable-http`, or `sse` |

Each tool module is independently togglable with its own switch — `APPTOOL`,
`USERSTOOL`, `HOUSEHOLDSTOOL`, `GROUPSTOOL`, `RECIPESTOOL`, `ORGANIZERTOOL`,
`SHAREDTOOL`, `ADMINTOOL`, `EXPLORETOOL`, `UTILSTOOL` (all default `True`). Observability
(`ENABLE_OTEL`, `OTEL_EXPORTER_OTLP_*`) and access governance (`EUNOMIA_TYPE`,
`EUNOMIA_POLICY_FILE`, `EUNOMIA_REMOTE_URL`) are optional. The full set is documented in
[`.env.example`](https://github.com/Knuckles-Team/mealie-mcp/blob/main/.env.example).
Copy it to `.env` and fill in only what you use.

## Docker Compose

The repo ships [`docker/mcp.compose.yml`](https://github.com/Knuckles-Team/mealie-mcp/blob/main/docker/mcp.compose.yml).
It reads a sibling `.env` and publishes the HTTP server on `:8000`:

```yaml
services:
  mealie-mcp-mcp:
    image: knucklessg1/mealie-mcp:latest
    container_name: mealie-mcp-mcp
    hostname: mealie-mcp-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
```

```bash
cp .env.example .env          # then edit MEALIE_* values
docker compose -f docker/mcp.compose.yml up -d
docker compose -f docker/mcp.compose.yml logs -f
```

## Agent server

`mealie-mcp` also ships an **A2A graph agent** (console script `mealie-agent`) that
connects to the MCP server and exposes a confidence-gated graph router plus an optional
web UI. The repo ships
[`docker/agent.compose.yml`](https://github.com/Knuckles-Team/mealie-mcp/blob/main/docker/agent.compose.yml),
which runs both the MCP server and the agent, wiring the agent to the MCP server with
`MCP_URL`:

```yaml
services:
  mealie-mcp-agent:
    image: knucklessg1/mealie-mcp:latest
    container_name: mealie-mcp-agent
    hostname: mealie-mcp-agent
    restart: always
    depends_on:
      - mealie-mcp-mcp
    env_file:
      - ../.env
    command: [ "mealie-agent" ]
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=9013
      - MCP_URL=http://mealie-mcp-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
    ports:
      - "9013:9013"
```

```bash
docker compose -f docker/agent.compose.yml up -d
curl -s http://localhost:9013/health         # {"status":"OK"}
```

The agent listens on `:9013` and reaches the MCP server by container name. Set
`PROVIDER` / `MODEL_ID` to select the language model backing the router.

## Behind a Caddy reverse proxy

Expose the HTTP server on a hostname with automatic TLS. Add to your `Caddyfile`:

```caddy
# Internal (self-signed) — homelab .arpa zone
mealie-mcp.arpa {
    tls internal
    reverse_proxy mealie-mcp-mcp:8000
}
```

```caddy
# Public — automatic Let's Encrypt
mealie-mcp.example.com {
    reverse_proxy mealie-mcp-mcp:8000
}
```

Reload Caddy:

```bash
docker compose -f services/caddy/compose.yml exec caddy caddy reload --config /etc/caddy/Caddyfile
```

## DNS with Technitium

Point the hostname at the host running Caddy. Via the Technitium API:

```bash
curl -s "http://technitium.arpa:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=mealie-mcp.arpa" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=10.0.0.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `mealie-mcp.arpa → <caddy-host-ip>` in the Technitium web
console (`http://technitium.arpa:5380`). The ecosystem
[`technitium-dns-mcp`](https://knuckles-team.github.io/technitium-dns-mcp/) automates
this as a tool.

## Register with an MCP client

Add to your client's `mcp_config.json`:

```json
{
  "mcpServers": {
    "mealie-mcp": {
      "command": "uv",
      "args": ["run", "mealie-mcp"],
      "env": {
        "MEALIE_BASE_URL": "https://your-mealie:9000",
        "MEALIE_TOKEN": "your_api_token",
        "MEALIE_SSL_VERIFY": "False"
      }
    }
  }
}
```

For a remote HTTP server, point the client at `http://mealie-mcp.arpa/mcp` instead.
