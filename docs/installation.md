# Installation

`mealie-mcp` is a standard Python package and a prebuilt container image. Pick the
path that matches how you want to run it.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable **Mealie instance** and an API token — see
  [Backing Platform](platform.md) to deploy one locally.

## From PyPI (recommended)

```bash
pip install mealie-mcp
```

### Optional extras

The base install ships the MCP server runtime. Install an extra for the agent or test
tooling:

| Extra | Install | Pulls in |
|---|---|---|
| *(base)* | `pip install mealie-mcp` | FastMCP MCP-server runtime (`agent-utilities[mcp]`) |
| `agent` | `pip install "mealie-mcp[agent]"` | Pydantic-AI agent + Logfire tracing (`agent-utilities[agent,logfire]`) |
| `all` | `pip install "mealie-mcp[all]"` | MCP server + agent + Logfire tracing |
| `test` | `pip install "mealie-mcp[test]"` | `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-xdist` |

```bash
# Typical: run the MCP server and the graph agent
pip install "mealie-mcp[all]"
```

## From source

```bash
git clone https://github.com/Knuckles-Team/mealie-mcp.git
cd mealie-mcp
pip install -e ".[all]"          # editable install with every extra
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv pip install -e ".[all]"
uv run mealie-mcp
```

## Prebuilt Docker image

A multi-stage, slim image is published on every release (entrypoint `mealie-mcp`):

```bash
docker pull knucklessg1/mealie-mcp:latest

docker run --rm -i \
  -e MEALIE_BASE_URL=https://your-mealie:9000 \
  -e MEALIE_TOKEN=your_api_token \
  knucklessg1/mealie-mcp:latest        # stdio transport (default)
```

For an HTTP server with a published port, see [Deployment](deployment.md).

## Verify the install

```bash
mealie-mcp --help
python -c "import mealie_mcp; print(mealie_mcp.__version__)"
```

## Next steps

- **[Deployment](deployment.md)** — run it as a long-lived MCP server (and agent) behind Caddy + DNS.
- **[Usage](usage.md)** — call the tools, the `Api` client, and the CLI.
- **[Configuration](deployment.md#configuration-environment)** — every environment variable.
