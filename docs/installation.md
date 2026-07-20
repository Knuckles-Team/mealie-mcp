# Installation

Choose the smallest runtime surface:

```bash
uvx --from "mealie-mcp[mcp]" mealie-mcp --help
uvx --from "mealie-mcp[agent]" mealie-agent --help
```

The `mcp` extra hosts the action-routed tools; the `agent` extra adds the model runtime. Configure package-index and certificate trust in the environment. Inject the Mealie endpoint and access token at launch rather than storing them in source or an MCP configuration file.

