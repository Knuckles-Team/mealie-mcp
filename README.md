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

*Version: 0.15.0*

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

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](file:///home/apps/workspace/agent-packages/agents/mealie-mcp/docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools
| Tool Module | Toggle Env Var | Enabled by Default | Description & Nested Methods |
|-------------|----------------|--------------------|------------------------------|
| **App** | `APPTOOL` | `True` | Manage mealie app operations. Action-routed methods: `get_startup_info`, `get_app_theme`. |
| **Users** | `USERSTOOL` | `True` | Manage mealie users operations. Action-routed methods: `get_token`, `oauth_login`, `oauth_callback`, `refresh_token`, `logout`, `register_new_user`, `get_logged_in_user`, `get_logged_in_user_ratings`, `get_logged_in_user_rating_for_recipe`, `get_logged_in_user_favorites`, `update_password`, `update_user`, `forgot_password`, `reset_password`, `update_user_image`, `create`, `delete`, `get_ratings`, `get_favorites`, `set_rating`, `add_favorite`, `remove_favorite`. |
| **Households** | `HOUSEHOLDSTOOL` | `True` | Manage mealie households operations. Action-routed methods: `get_households_cookbooks`, `post_households_cookbooks`, `put_households_cookbooks`, `get_households_cookbooks_item_id`, `put_households_cookbooks_item_id`, `delete_households_cookbooks_item_id`, `get_households_events_notifications`, `post_households_events_notifications`, `get_households_events_notifications_item_id`, `put_households_events_notifications_item_id`, `delete_households_events_notifications_item_id`, `test_notification`, `get_households_recipe_actions`, `post_households_recipe_actions`, `get_households_recipe_actions_item_id`, `put_households_recipe_actions_item_id`, `delete_households_recipe_actions_item_id`, `trigger_action`, `get_logged_in_user_household`, `get_household_recipe`, `get_household_members`, `get_household_preferences`, `update_household_preferences`, `set_member_permissions`, `get_statistics`, `get_invite_tokens`, `create_invite_token`, `email_invitation`, `get_households_shopping_lists`, `post_households_shopping_lists`, `get_households_shopping_lists_item_id`, `put_households_shopping_lists_item_id`, `delete_households_shopping_lists_item_id`, `update_label_settings`, `add_recipe_ingredients_to_list`, `add_single_recipe_ingredients_to_list`, `remove_recipe_ingredients_from_list`, `get_households_shopping_items`, `post_households_shopping_items`, `put_households_shopping_items`, `delete_households_shopping_items`, `post_households_shopping_items_create_bulk`, `get_households_shopping_items_item_id`, `put_households_shopping_items_item_id`, `delete_households_shopping_items_item_id`, `get_households_webhooks`, `post_households_webhooks`, `rerun_webhooks`, `get_households_webhooks_item_id`, `put_households_webhooks_item_id`, `delete_households_webhooks_item_id`, `test_one`, `get_households_mealplans_rules`, `post_households_mealplans_rules`, `get_households_mealplans_rules_item_id`, `put_households_mealplans_rules_item_id`, `delete_households_mealplans_rules_item_id`, `get_households_mealplans`, `post_households_mealplans`, `get_todays_meals`, `create_random_meal`, `get_households_mealplans_item_id`, `put_households_mealplans_item_id`, `delete_households_mealplans_item_id`. |
| **Groups** | `GROUPSTOOL` | `True` | Manage mealie groups operations. Action-routed methods: `get_all_households`, `get_one_household`, `get_logged_in_user_group`, `get_group_members`, `get_group_member`, `get_group_preferences`, `update_group_preferences`, `get_storage`, `start_data_migration`, `get_groups_reports`, `get_groups_reports_item_id`, `delete_groups_reports_item_id`, `get_groups_labels`, `post_groups_labels`, `get_groups_labels_item_id`, `put_groups_labels_item_id`, `delete_groups_labels_item_id`, `seed_foods`, `seed_labels`, `seed_units`. |
| **Recipes** | `RECIPESTOOL` | `True` | Manage mealie recipes operations. Action-routed methods: `get_recipe_formats_and_templates`, `get_recipe_as_format`, `test_parse_recipe_url`, `create_recipe_from_html_or_json`, `parse_recipe_url`, `parse_recipe_url_bulk`, `create_recipe_from_zip`, `create_recipe_from_image`, `get_recipes`, `post_recipes`, `put_recipes`, `patch_many`, `get_recipes_suggestions`, `get_recipes_slug`, `put_recipes_slug`, `patch_one`, `delete_recipes_slug`, `duplicate_one`, `update_last_made`, `scrape_image_url`, `update_recipe_image`, `delete_recipe_image`, `upload_recipe_asset`, `get_recipe_comments`, `bulk_tag_recipes`, `bulk_settings_recipes`, `bulk_categorize_recipes`, `bulk_delete_recipes`, `bulk_export_recipes`, `get_exported_data`, `get_exported_data_token`, `purge_export_data`, `get_shared_recipe`, `get_shared_recipe_as_zip`, `get_recipes_timeline_events`, `post_recipes_timeline_events`, `get_recipes_timeline_events_item_id`, `put_recipes_timeline_events_item_id`, `delete_recipes_timeline_events_item_id`, `update_event_image`, `get_comments`, `post_comments`, `get_comments_item_id`, `put_comments_item_id`, `post_parser_ingredient`, `parse_ingredient`, `parse_ingredients`, `get_foods`, `post_foods`, `put_foods_merge`, `get_foods_item_id`, `put_foods_item_id`, `delete_foods_item_id`, `get_units`, `post_units`, `put_units_merge`, `get_units_item_id`, `put_units_item_id`, `delete_units_item_id`, `get_recipe_img`, `get_recipe_timeline_event_img`, `get_recipe_asset`, `get_user_image`, `get_validation_text`. |
| **Organizer** | `ORGANIZERTOOL` | `True` | Manage mealie organizer operations. Action-routed methods: `get_organizers_categories`, `post_organizers_categories`, `get_all_empty`, `get_organizers_categories_item_id`, `put_organizers_categories_item_id`, `delete_organizers_categories_item_id`, `get_organizers_categories_slug_category_slug`, `get_organizers_tags`, `post_organizers_tags`, `get_empty_tags`, `get_organizers_tags_item_id`, `put_organizers_tags_item_id`, `delete_recipe_tag`, `get_organizers_tags_slug_tag_slug`, `get_organizerss`, `post_organizerss`, `get_organizerss_item_id`, `put_organizerss_item_id`, `delete_organizerss_item_id`, `get_organizerss_slug_slug`. |
| **Shared** | `SHAREDTOOL` | `True` | Manage mealie shared operations. Action-routed methods: `get_shared_recipes`, `post_shared_recipes`, `get_shared_recipes_item_id`, `delete_shared_recipes_item_id`. |
| **Admin** | `ADMINTOOL` | `True` | Manage mealie admin operations. Action-routed methods: `get_app_info`, `get_app_statistics`, `check_app_config`, `get_admin_users`, `post_admin_users`, `unlock_users`, `get_admin_users_item_id`, `put_admin_users_item_id`, `delete_admin_users_item_id`, `generate_token`, `get_admin_households`, `post_admin_households`, `get_admin_households_item_id`, `put_admin_households_item_id`, `delete_admin_households_item_id`, `get_admin_groups`, `post_admin_groups`, `get_admin_groups_item_id`, `put_admin_groups_item_id`, `delete_admin_groups_item_id`, `check_email_config`, `send_test_email`, `get_admin_backups`, `post_admin_backups`, `get_admin_backups_file_name`, `delete_admin_backups_file_name`, `upload_one`, `import_one`, `get_maintenance_summary`, `get_storage_details`, `clean_images`, `clean_temp`, `clean_recipe_folders`, `debug_openai`. |
| **Explore** | `EXPLORETOOL` | `True` | Manage mealie explore operations. Action-routed methods: `get_explore_groups_group_slug_foods`, `get_explore_groups_group_slug_foods_item_id`, `get_explore_groups_group_slug_households`, `get_household`, `get_explore_groups_group_slug_organizers_categories`, `get_explore_groups_group_slug_organizers_categories_item_id`, `get_explore_groups_group_slug_organizers_tags`, `get_explore_groups_group_slug_organizers_tags_item_id`, `get_explore_groups_group_slug_organizerss`, `get_explore_groups_group_slug_organizerss_item_id`, `get_explore_groups_group_slug_cookbooks`, `get_explore_groups_group_slug_cookbooks_item_id`, `get_explore_groups_group_slug_recipes`, `get_explore_groups_group_slug_recipes_suggestions`, `get_recipe`. |
| **Utils** | `UTILSTOOL` | `True` | Manage mealie utils operations. Action-routed methods: `download_file`. |

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/mcp.md](file:///home/apps/workspace/agent-packages/agents/mealie-mcp/docs/mcp.md).

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

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/agent.md](file:///home/apps/workspace/agent-packages/agents/mealie-mcp/docs/agent.md).

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
