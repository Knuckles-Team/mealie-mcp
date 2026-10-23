# CONN-MEALIE-MCP-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `mealie-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `mealie_mcp` from it.
