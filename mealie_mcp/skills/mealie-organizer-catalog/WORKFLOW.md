# Mealie Organizer Catalog

Maintain the Mealie taxonomy via the mealie-mcp MCP server — categories, tags and tools with the `mealie_organizer` tool, plus the foods and units catalog on the `mealie_recipes` tool. Use when the agent must list/create/rename/merge the labels recipes are filed under, curate the reusable food and unit entities, or clean up empty/duplicate organizers. Do NOT use for recipe CRUD/import (use mealie-recipe-management) or meal plans/cookbooks/shopping lists (use mealie-meal-planning); prefer those.

Domain-typed access to the Mealie **organizer taxonomy** (categories, tags, tools)
and the **foods / units** catalog. Prefer the condensed tools over raw HTTP.

## When to use
- List / create / rename / delete **categories**, **tags** and recipe **tools**.
- Curate the shared **foods** and **units** catalog, including merging duplicates
  (`put_foods_merge`, `put_units_merge`).
- Find and prune **empty** organizers (`get_all_empty`, `get_empty_tags`).
- Look up an organizer by its **slug** (`get_organizers_categories_slug_category_slug`, etc.).

## When NOT to use
- Recipe CRUD/import → `mealie-recipe-management`.
- Meal plans, cookbooks, shopping lists, household prefs → `mealie-meal-planning`.
- Public/unauthenticated browsing of another group's organizers → the
  `mealie_explore` tool.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`mealie-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `MEALIE_BASE_URL` | ✅ | Base URL of the Mealie instance |
| `MEALIE_TOKEN` | ✅ | Long-lived API token |
| `MEALIE_TLS_PROFILE[_REF]` | optional | Runtime TLS profile for private PKI, mTLS, or proxy policy |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface vs.
the one-to-one verbose tools.

## Tools & actions
Prefer the **condensed** tool; `action` + a `params_json` **JSON string**.

| Condensed tool | Key actions |
|----------------|-------------|
| `mealie_organizer` | `get_organizers_categories`, `post_organizers_categories`, `put_organizers_categories_item_id`, `delete_organizers_categories_item_id`, `get_organizers_tags`, `post_organizers_tags`, `get_organizers_tools`, `post_organizers_tools`, `get_all_empty`, `get_empty_tags` |
| `mealie_recipes` | `get_foods`, `post_foods`, `put_foods_item_id`, `put_foods_merge`, `get_units`, `post_units`, `put_units_item_id`, `put_units_merge` |

### Key parameters
- `item_id` — the category / tag / tool / food / unit id for get-one/put/delete.
- `data` — body for creates/updates (e.g. `{"name": "..."}`).
- Merge actions (`put_foods_merge` / `put_units_merge`) take a `from`/`to` id pair
  in `data` — the `from` entity is deleted and its recipe references repointed.

## Recipes (`params_json`)
Create a category:
```json
{"data":{"name":"Dinner"}}
```
Merge two duplicate foods:
```json
{"data":{"fromFood":"<food-uuid-a>","toFood":"<food-uuid-b>"}}
```
Find empty (unused) tags:
```json
{}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object.
- Merging is **destructive** — the `from` entity is deleted; confirm intent
  before merging foods/units.
- Categories/tags/tools are **group-scoped**, not household-scoped.
- Deleting a category/tag/tool still in use on recipes un-tags those recipes; it
  does not delete the recipes themselves.

## Related
- `mealie-recipe-management` assigns these categories/tags/tools/foods/units to
  recipes.
- `mealie-meal-planning` cookbooks filter on the categories/tags defined here.
