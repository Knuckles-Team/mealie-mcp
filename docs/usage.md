# Usage — API / CLI / MCP

`mealie-mcp` exposes the same capability three ways: as **MCP tools** an agent calls,
as a **Python API** (`Api`) you import, and as a **CLI** entry point. The complete tool
surface and the agent-package layout are in [Overview](overview.md).

## As an MCP server

Once [deployed](deployment.md), the server registers one action-routed tool module per
Mealie domain. Reads work with a Mealie connection and an API token; each module is
independently togglable with its own switch (`RECIPESTOOL`, `USERSTOOL`, …).

| Tool module | Toggle | Surface |
|---|---|---|
| `app` | `APPTOOL` | App theme, startup info |
| `users` | `USERSTOOL` | Users, favorites, ratings, tokens |
| `households` | `HOUSEHOLDSTOOL` | Cookbooks, meal plans, shopping lists, webhooks |
| `groups` | `GROUPSTOOL` | Group members, labels, reports, storage |
| `recipes` | `RECIPESTOOL` | Recipes, exports, scraping, timeline events |
| `organizer` | `ORGANIZERTOOL` | Categories, tags, tools |
| `shared` | `SHAREDTOOL` | Shared-recipe operations |
| `admin` | `ADMINTOOL` | Administration operations |
| `explore` | `EXPLORETOOL` | Public explore endpoints |
| `utils` | `UTILSTOOL` | Utility/maintenance operations |

Example agent prompts that map onto these tools:

- *"Find recipes that match 'chicken'"* → `recipes`
- *"Add the ingredients of recipe `<slug>` to my shopping list"* → `households`
- *"Show this week's meal plan"* → `households`

## As a Python API

`Api` is a `requests`-based facade composed from the Mealie service domains. Construct it
directly, or build it from the environment with `get_client()`.

```python
from mealie_mcp.api_client import Api

api = Api(
    base_url="https://your-mealie:9000",
    token="your_api_token",
    verify=False,
)

# Reads
recipes = api.get_recipes()                      # paginated recipe records
recipe = api.get_recipes_slug("classic-pancakes")
user = api.get_logged_in_user()
theme = api.get_app_theme()
```

Build a client straight from the environment:

```python
from mealie_mcp.auth import get_client
api = get_client()        # reads MEALIE_BASE_URL / MEALIE_TOKEN / MEALIE_SSL_VERIFY
```

### Writes

Write methods follow the same client; they require a token with write permission on the
target Mealie instance:

```python
api.parse_recipe_url({"url": "https://example.com/recipes/pancakes"})
api.create_recipe_from_html_or_json({"data": "<html>…</html>"})
```

## As a CLI

The `mealie-mcp` console script is the MCP server entry point and accepts the transport
flags directly:

```bash
mealie-mcp --help
mealie-mcp                                           # stdio (default)
mealie-mcp --transport streamable-http --port 8000   # network server
```

The `mealie-agent` console script launches the A2A graph agent (see
[Deployment](deployment.md#agent-server)):

```bash
mealie-agent --help
```
