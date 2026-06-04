# Mealie Mcp
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/mealie-mcp)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/mealie-mcp)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/mealie-mcp)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/mealie-mcp)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/mealie-mcp)
![PyPI - License](https://img.shields.io/pypi/l/mealie-mcp)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/mealie-mcp)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/mealie-mcp)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/mealie-mcp)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/mealie-mcp)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/mealie-mcp)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/mealie-mcp)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/mealie-mcp)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/mealie-mcp)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/mealie-mcp)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/mealie-mcp)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/mealie-mcp)

*Version: 0.38.0*

---

## Overview

**Mealie Mcp** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with Mealie MCP Server for Agentic AI!.

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Comprehensive support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the Mealie MCP Server for Agentic AI! API. You can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools
| Tool Module | Toggle Env Var | Enabled by Default | Description & Nested Methods |
|-------------|----------------|--------------------|------------------------------|
| **App** | `APP_TOOL` | `True` | Manage mealie app operations. Action-routed methods: `get_app_theme`, `get_startup_info`. |
| **Users** | `USERS_TOOL` | `True` | Manage mealie users operations. Action-routed methods: `add_favorite`, `create`, `delete`, `forgot_password`, `get_favorites`, `get_logged_in_user`, `get_logged_in_user_favorites`, `get_logged_in_user_rating_for_recipe`, `get_logged_in_user_ratings`, `get_ratings`, `get_token`, `logout`, `oauth_callback`, `oauth_login`, `refresh_token`, `register_new_user`, `remove_favorite`, `reset_password`, `set_rating`, `update_password`, `update_user`, `update_user_image`. |
| **Households** | `HOUSEHOLDS_TOOL` | `True` | Manage mealie households operations. Action-routed methods: `add_recipe_ingredients_to_list`, `add_single_recipe_ingredients_to_list`, `create_invite_token`, `create_random_meal`, `delete_households_cookbooks_item_id`, `delete_households_events_notifications_item_id`, `delete_households_mealplans_item_id`, `delete_households_mealplans_rules_item_id`, `delete_households_recipe_actions_item_id`, `delete_households_shopping_items`, `delete_households_shopping_items_item_id`, `delete_households_shopping_lists_item_id`, `delete_households_webhooks_item_id`, `email_invitation`, `get_household_members`, `get_household_preferences`, `get_household_recipe`, `get_households_cookbooks`, `get_households_cookbooks_item_id`, `get_households_events_notifications`, `get_households_events_notifications_item_id`, `get_households_mealplans`, `get_households_mealplans_item_id`, `get_households_mealplans_rules`, `get_households_mealplans_rules_item_id`, `get_households_recipe_actions`, `get_households_recipe_actions_item_id`, `get_households_shopping_items`, `get_households_shopping_items_item_id`, `get_households_shopping_lists`, `get_households_shopping_lists_item_id`, `get_households_webhooks`, `get_households_webhooks_item_id`, `get_invite_tokens`, `get_logged_in_user_household`, `get_statistics`, `get_todays_meals`, `post_households_cookbooks`, `post_households_events_notifications`, `post_households_mealplans`, `post_households_mealplans_rules`, `post_households_recipe_actions`, `post_households_shopping_items`, `post_households_shopping_items_create_bulk`, `post_households_shopping_lists`, `post_households_webhooks`, `put_households_cookbooks`, `put_households_cookbooks_item_id`, `put_households_events_notifications_item_id`, `put_households_mealplans_item_id`, `put_households_mealplans_rules_item_id`, `put_households_recipe_actions_item_id`, `put_households_shopping_items`, `put_households_shopping_items_item_id`, `put_households_shopping_lists_item_id`, `put_households_webhooks_item_id`, `remove_recipe_ingredients_from_list`, `rerun_webhooks`, `set_member_permissions`, `test_notification`, `test_one`, `trigger_action`, `update_household_preferences`, `update_label_settings`. |
| **Groups** | `GROUPS_TOOL` | `True` | Manage mealie groups operations. Action-routed methods: `delete_groups_labels_item_id`, `delete_groups_reports_item_id`, `get_all_households`, `get_group_member`, `get_group_members`, `get_group_preferences`, `get_groups_labels`, `get_groups_labels_item_id`, `get_groups_reports`, `get_groups_reports_item_id`, `get_logged_in_user_group`, `get_one_household`, `get_storage`, `post_groups_labels`, `put_groups_labels_item_id`, `seed_foods`, `seed_labels`, `seed_units`, `start_data_migration`, `update_group_preferences`. |
| **Recipes** | `RECIPES_TOOL` | `True` | Manage mealie recipes operations. Action-routed methods: `bulk_categorize_recipes`, `bulk_delete_recipes`, `bulk_export_recipes`, `bulk_settings_recipes`, `bulk_tag_recipes`, `create_recipe_from_html_or_json`, `create_recipe_from_image`, `create_recipe_from_zip`, `delete_foods_item_id`, `delete_recipe_image`, `delete_recipes_slug`, `delete_recipes_timeline_events_item_id`, `delete_units_item_id`, `duplicate_one`, `get_comments`, `get_comments_item_id`, `get_exported_data`, `get_exported_data_token`, `get_foods`, `get_foods_item_id`, `get_recipe_as_format`, `get_recipe_asset`, `get_recipe_comments`, `get_recipe_formats_and_templates`, `get_recipe_img`, `get_recipe_timeline_event_img`, `get_recipes`, `get_recipes_slug`, `get_recipes_suggestions`, `get_recipes_timeline_events`, `get_recipes_timeline_events_item_id`, `get_shared_recipe`, `get_shared_recipe_as_zip`, `get_units`, `get_units_item_id`, `get_user_image`, `get_validation_text`, `parse_ingredient`, `parse_ingredients`, `parse_recipe_url`, `parse_recipe_url_bulk`, `patch_many`, `patch_one`, `post_comments`, `post_foods`, `post_parser_ingredient`, `post_recipes`, `post_recipes_timeline_events`, `post_units`, `purge_export_data`, `put_comments_item_id`, `put_foods_item_id`, `put_foods_merge`, `put_recipes`, `put_recipes_slug`, `put_recipes_timeline_events_item_id`, `put_units_item_id`, `put_units_merge`, `scrape_image_url`, `test_parse_recipe_url`, `update_event_image`, `update_last_made`, `update_recipe_image`, `upload_recipe_asset`. |
| **Organizer** | `ORGANIZER_TOOL` | `True` | Manage mealie organizer operations. Action-routed methods: `delete_organizers_categories_item_id`, `delete_organizerss_item_id`, `delete_recipe_tag`, `get_all_empty`, `get_empty_tags`, `get_organizers_categories`, `get_organizers_categories_item_id`, `get_organizers_categories_slug_category_slug`, `get_organizers_tags`, `get_organizers_tags_item_id`, `get_organizers_tags_slug_tag_slug`, `get_organizerss`, `get_organizerss_item_id`, `get_organizerss_slug_slug`, `post_organizers_categories`, `post_organizers_tags`, `post_organizerss`, `put_organizers_categories_item_id`, `put_organizers_tags_item_id`, `put_organizerss_item_id`. |
| **Shared** | `SHARED_TOOL` | `True` | Manage mealie shared operations. Action-routed methods: `delete_shared_recipes_item_id`, `get_shared_recipes`, `get_shared_recipes_item_id`, `post_shared_recipes`. |
| **Admin** | `ADMIN_TOOL` | `True` | Manage mealie admin operations. Action-routed methods: `check_app_config`, `check_email_config`, `clean_images`, `clean_recipe_folders`, `clean_temp`, `debug_openai`, `delete_admin_backups_file_name`, `delete_admin_groups_item_id`, `delete_admin_households_item_id`, `delete_admin_users_item_id`, `generate_token`, `get_admin_backups`, `get_admin_backups_file_name`, `get_admin_groups`, `get_admin_groups_item_id`, `get_admin_households`, `get_admin_households_item_id`, `get_admin_users`, `get_admin_users_item_id`, `get_app_info`, `get_app_statistics`, `get_maintenance_summary`, `get_storage_details`, `import_one`, `post_admin_backups`, `post_admin_groups`, `post_admin_households`, `post_admin_users`, `put_admin_groups_item_id`, `put_admin_households_item_id`, `put_admin_users_item_id`, `send_test_email`, `unlock_users`, `upload_one`. |
| **Explore** | `EXPLORE_TOOL` | `True` | Manage mealie explore operations. Action-routed methods: `get_explore_groups_group_slug_cookbooks`, `get_explore_groups_group_slug_cookbooks_item_id`, `get_explore_groups_group_slug_foods`, `get_explore_groups_group_slug_foods_item_id`, `get_explore_groups_group_slug_households`, `get_explore_groups_group_slug_organizers_categories`, `get_explore_groups_group_slug_organizers_categories_item_id`, `get_explore_groups_group_slug_organizers_tags`, `get_explore_groups_group_slug_organizers_tags_item_id`, `get_explore_groups_group_slug_organizerss`, `get_explore_groups_group_slug_organizerss_item_id`, `get_explore_groups_group_slug_recipes`, `get_explore_groups_group_slug_recipes_suggestions`, `get_household`, `get_recipe`. |
| **Utils** | `UTILS_TOOL` | `True` | Manage mealie utils operations. Action-routed methods: `download_file`. |

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/mcp.md](docs/mcp.md).

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows you to restrict the set of exposed tools in order to prevent blowing up the LLM's context window.

You can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to your transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

### MCP Configuration Examples

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "mealie-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "mealie-mcp",
        "mealie-mcp"
      ],
      "env": {
        "MEALIE_ENDPOINT": "your_mealie_endpoint_here",
        "MEALIE_API_KEY": "your_mealie_api_key_here"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (Recommended for production deployments)
Configure your client's `mcp.json` to launch the Streamable-HTTP server via `uvx` with explicit host and port definition:

```json
{
  "mcpServers": {
    "mealie-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "mealie-mcp",
        "mealie-mcp"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "MEALIE_ENDPOINT": "your_mealie_endpoint_here",
        "MEALIE_API_KEY": "your_mealie_api_key_here"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed remote or local Streamable-HTTP instance:

```json
{
  "mcpServers": {
    "mealie-mcp": {
      "url": "http://localhost:8000/mealie-mcp/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name mealie-mcp-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e MEALIE_ENDPOINT="your_value" \
  -e MEALIE_API_KEY="your_value" \
  knucklessg1/mealie-mcp:latest
```

---

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export MEALIE_ENDPOINT="your_value"
export MEALIE_API_KEY="your_value"

# Run the agent server
mealie-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

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
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

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
      - ENABLE_OTEL=True
    ports:
      - "9013:9013"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:9013/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

```

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/agent.md](docs/agent.md).

---

## Security & Governance

Built directly upon the enterprise-ready [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) core, standard security parameters are fully supported:

### Access Control & Policy Enforcement
- **Eunomia Policies:** Fine-grained, policy-driven tool authorization. Supports `none`, local `embedded` (`mcp_policies.json`), or centralized `remote` modes.
- **OIDC Token Delegation:** Compliant with RFC 8693 token exchange for flowing authenticating user credentials from Web UI / ACP → Agent → MCP.
- **Scoped Credentials:** Execution context runs restricted to the specific caller identity.

### Runtime Security Grid
| Feature | Functionality | Enablement |
|---------|---------------|------------|
| **Tool Guard** | Sensitivity inspection with human-in-the-loop validation | Enabled by default |
| **Prompt Injection Defense** | Input scanning, repetition monitoring, and recursive loop blocks | Enabled by default |
| **Context Safety Guard** | Stuck-loop detectors and contextual overflow preemptive alerts | Enabled by default |

---

## Installation

Install the Python package locally:

```bash
# Using uv (highly recommended)
uv pip install mealie-mcp[all]

# Using standard pip
python -m pip install mealie-mcp[all]
```

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`
