# Mealie Organizer Catalog

Maintain the Mealie taxonomy via the mealie-mcp MCP server — categories, tags and tools with the `mealie_organizer` tool, plus the foods and units catalog on the `mealie_recipes` tool. Use when the agent must list/create/rename/merge the labels recipes are filed under, curate the reusable food and unit entities, or clean up empty/duplicate organizers. Do NOT use for recipe CRUD/import (use mealie-recipe-management) or meal plans/cookbooks/shopping lists (use mealie-meal-planning); prefer those.

# Mealie Organizer Catalog

Domain-typed access to the Mealie **organizer taxonomy** (categories, tags, tools)
and the **foods / units** catalog. Prefer the condensed tools over raw HTTP.

## When to use
- List / create / rename / delete recipe **categories**, **tags** and **tools**
  (`mealie_organizer`).
- Find **empty** organizers to prune (`get_all_empty`, `get_empty_tags`).
- Manage the reusable **foods** and **units** catalog, including **merge**
  (`put_foods_merge`, `put_units_merge`) to dedupe (`mealie_recipes`).

## When NOT to use
- Creating/editing recipes or attaching tags to a specific recipe →
  `mealie-recipe-management` (bulk tag/categorize live there).
- Meal plans, cookbooks, shopping lists → `mealie-meal-planning`.
- Users/groups/admin → the `mealie_users` / `mealie_groups` / `mealie_admin` tools.

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
Prefer the **condensed** tools; `action` + a `params_json` **JSON string**.

| Condensed tool | Key actions |
|----------------|-------------|
| `mealie_organizer` | `get_organizers_categories`, `post_organizers_categories`, `put_organizers_categories_item_id`, `get_all_empty`, `get_organizers_tags`, `post_organizers_tags`, `get_empty_tags`, `get_organizers_tools`, `post_organizers_tools` |
| `mealie_recipes` | `get_foods`, `post_foods`, `put_foods_merge`, `get_units`, `post_units`, `put_units_merge` |

### Key parameters
- `data` — body for creates: a category/tag/tool needs `{"name":"..."}`.
- `item_id` — the category/tag/tool/food/unit id for get/put/delete.
- merges take a body naming the **fromId** and **toId** entities to combine.

## Recipes (`params_json`)
List all categories:
```json
{}
```
Create a tag:
```json
{"data":{"name":"Weeknight"}}
```
Merge two duplicate foods into one:
```json
{"data":{"fromFood":"<dup-food-uuid>","toFood":"<canonical-food-uuid>"}}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object.
- Categories/tags/tools each expose their own list, item and slug lookups — a
  **slug** is derived from the name; renaming changes the slug and can break saved
  cookbook filters that reference it.
- Deleting a category/tag does **not** delete recipes; it only unfiles them —
  check `get_all_empty` / `get_empty_tags` before pruning.
- **Merge is destructive and irreversible**: `put_foods_merge` / `put_units_merge`
  re-point every ingredient from the source entity to the target, then remove the
  source.
- Foods and units live on the **`mealie_recipes`** tool, not `mealie_organizer`.

## Related
- `mealie-recipe-management` files recipes under these categories/tags/tools and
  references these foods/units in ingredients.
- `mealie-meal-planning` cookbooks are defined by filters over this taxonomy.
