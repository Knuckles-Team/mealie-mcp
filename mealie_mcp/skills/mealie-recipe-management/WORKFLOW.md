# Mealie Recipe Management

Recipe CRUD and import on Mealie via the mealie-mcp MCP server — list/search recipes, read one by slug, create from a URL/HTML/image, update, duplicate, and manage recipe images with the domain-typed `mealie_recipes` tool. Use when the agent must browse or search the recipe catalog, import a recipe from the web or a photo, edit recipe fields, or push recipes into the knowledge graph. Do NOT use for meal-plan scheduling, cookbooks or shopping lists (use mealie-meal-planning) or for categories/tags/tools/foods/units taxonomy (use mealie-organizer-catalog); prefer those.

# Mealie Recipe Management

Domain-typed access to the Mealie **recipes** surface for browsing, importing and
editing recipes. Prefer the condensed `mealie_recipes` tool over raw HTTP — it
carries the recipe field conventions and returns recipe-shaped records.

## When to use
- List / search / paginate the recipe catalog (by category, tag, tool, food).
- Fetch a single recipe by `slug` (full body with ingredients + instructions).
- Import a recipe from a URL (`parse_recipe_url`), HTML/JSON, a ZIP, or a photo
  (`create_recipe_from_image`).
- Edit a recipe (`put_recipes_slug` / `patch_one`), duplicate it, mark
  `update_last_made`, or manage its image (`scrape_image_url`, `update_recipe_image`).
- Natively ingest recipes into the knowledge graph (`mealie_ingest_recipes`).

## When NOT to use
- Meal-plan entries, cookbooks, shopping lists, household prefs →
  `mealie-meal-planning`.
- Category / tag / tool / food / unit taxonomy management →
  `mealie-organizer-catalog`.
- Users, groups, admin, or app/startup info → the `mealie_users` / `mealie_groups`
  / `mealie_admin` / `mealie_app` tools directly.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`mealie-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `MEALIE_BASE_URL` | ✅ | Base URL of the Mealie instance |
| `MEALIE_TOKEN` | ✅ | Long-lived API token (Settings → API Tokens) |
| `MEALIE_TLS_PROFILE[_REF]` | optional | Runtime TLS profile for private PKI, mTLS, or proxy policy |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface (used
below) vs. the one-to-one verbose tools.

## Tools & actions
Prefer the **condensed** tool; it takes `action` + a `params_json` **JSON string**
whose keys are passed straight to the client method.

| Condensed tool | Key actions |
|----------------|-------------|
| `mealie_recipes` | `get_recipes`, `get_recipes_slug`, `parse_recipe_url`, `create_recipe_from_html_or_json`, `create_recipe_from_image`, `post_recipes`, `put_recipes_slug`, `patch_one`, `duplicate_one`, `update_last_made`, `scrape_image_url`, `bulk_tag_recipes` |
| `mealie_ingest_recipes` | native KG ingestion (typed `:Recipe` + `:Ingredient` + image blobs) |

### Key parameters
- `slug` — required for `get_recipes_slug`, `put_recipes_slug`, `patch_one`.
- `search`, `categories`, `tags`, `tools`, `foods`, `page`, `per_page`,
  `order_by`, `order_direction` — `get_recipes` filters/pagination.
- `data` — object body for creates/updates (`parse_recipe_url` takes
  `{"url": "..."}`; `post_recipes` takes `{"name": "..."}`).

## Recipes (`params_json`)
List recipes matching a search, newest first, small page:
```json
{"search":"pasta","order_by":"created_at","order_direction":"desc","per_page":25}
```
Read one full recipe by slug:
```json
{"slug":"spaghetti-carbonara"}
```
Import a recipe from the web:
```json
{"data":{"url":"[configured-endpoint]
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- `get_recipes` returns a **paginated envelope** `{"items":[...],"page","per_page","total"}`
  — read the `items` array, not the top-level object.
- Most write/read-by-id actions key off the **`slug`**, not the UUID `id`; get the
  slug from a `get_recipes` item first.
- `create_recipe_from_image` / `create_recipe_from_zip` take multipart uploads —
  provide the file via the client's `data`/`files` convention, not a JSON body.
- Creating a recipe often returns just the new **slug string**; re-read with
  `get_recipes_slug` to get the full body.

## Related
- `mealie_ingest_recipes` pulls recipes into the knowledge graph as typed
  `:Recipe`/`:Ingredient`/`:Food`/`:Unit` nodes (+ optional `:AssetOccurrence` image
  blobs); use it for ingestion, not for the browse/edit recipes above.
- **Downstream:** `mealie-meal-planning` schedules these recipes;
  `mealie-organizer-catalog` maintains the categories/tags they are filed under.
