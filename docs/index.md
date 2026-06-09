# mealie-mcp

Mealie recipe-manager **API + MCP Server + A2A Agent** for the agent-utilities
ecosystem — a typed, deterministic tool surface over the
[Mealie](https://mealie.io/) self-hosted recipe and meal-planning platform.

!!! info "Official documentation"
    This site is the canonical reference for `mealie-mcp`, maintained alongside every
    release.

[![PyPI](https://img.shields.io/pypi/v/mealie-mcp)](https://pypi.org/project/mealie-mcp/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/mealie-mcp)](https://github.com/Knuckles-Team/mealie-mcp/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/mealie-mcp)

## Overview

`mealie-mcp` wraps the Mealie REST API with consolidated, action-routed MCP tools and
ships an optional Pydantic-AI graph agent. It provides:

- **`Api`** — a tolerant `requests`-based REST client composed from the Mealie service
  domains (app, users, households, groups, recipes, organizer, shared, admin, explore,
  utils).
- **Action-routed MCP tools** — one togglable tool module per domain, keeping the LLM
  tool surface compact and IDE-compatible.
- **An A2A graph agent** (`mealie-agent`) — a confidence-gated router that activates only
  the tools relevant to each query, preserving model context.

The server remains inactive when credentials are absent: reads and writes require a
reachable Mealie endpoint and an API token.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-launch: **[Installation](installation.md)** — pip, source, extras, and the prebuilt Docker image.
- :material-server-network: **[Deployment](deployment.md)** — run the MCP and agent servers, Docker Compose, Caddy + Technitium.
- :material-console: **[Usage](usage.md)** — the MCP tools, the `Api` client, and the CLI.
- :material-database-cog: **[Backing Platform](platform.md)** — deploy Mealie with Docker.
- :material-sitemap: **[Overview](overview.md)** — the layered client and agent-package pattern.
- :material-tag-multiple: **[Concepts](concepts.md)** — the `CONCEPT:MEAL-*` registry.

</div>

## Quick start

```bash
pip install mealie-mcp
mealie-mcp                       # stdio MCP server (default transport)
```

Connect it to a Mealie instance:

```bash
export MEALIE_BASE_URL=https://your-mealie:9000
export MEALIE_TOKEN=your_api_token
mealie-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

See **[Installation](installation.md)** and **[Deployment](deployment.md)** for the
full matrix (PyPI extras, Docker image, all transports, the agent server, reverse
proxy, DNS).
