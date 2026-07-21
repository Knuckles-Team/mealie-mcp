---
name: mealie-meal-planning
skill_type: skill
description: >-
  Household meal planning, cookbooks and shopping lists on Mealie via the
  mealie-mcp MCP server — schedule recipes onto dates, browse/get today's meals,
  build cookbooks, and manage shopping lists and their items with the
  domain-typed `mealie_households` tool. Use when the agent must plan meals for a
  date range, generate a random meal, assemble a shopping list from recipe
  ingredients, or read household cookbooks. Do NOT use for recipe CRUD/import
  (use mealie-recipe-management) or for category/tag/food/unit taxonomy (use
  mealie-organizer-catalog); prefer those.
license: MIT
tags: [mealie, meal-plan, cookbook, shopping-list, household, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Mealie Meal Planning

Domain-typed access to the Mealie **households** surface — meal plans, cookbooks
and shopping lists. Prefer the condensed `mealie_households` tool over raw HTTP.

## When to use
- Schedule a recipe onto a date (`post_households_mealplans`), read a date range
  (`get_households_mealplans`), or fetch `get_todays_meals` / `create_random_meal`.
- Create and manage **cookbooks** (filter-defined recipe collections).
- Build and edit **shopping lists** and their items, including
  `add_recipe_ingredients_to_list` to seed a list from a recipe.
- Read household members, preferences and statistics.

## When NOT to use
- Creating, importing or editing the recipes themselves →
  `mealie-recipe-management`.
- Category / tag / tool / food / unit taxonomy → `mealie-organizer-catalog`.
- Public/unauthenticated browsing of another group's data → the `mealie_explore`
  tool.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`mealie-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `MEALIE_BASE_URL` | ✅ | Base URL of the Mealie instance |
| `MEALIE_TOKEN` | ✅ | Long-lived API token; the token's user fixes the household |
| `MEALIE_TLS_PROFILE[_REF]` | optional | Runtime TLS profile for private PKI, mTLS, or proxy policy |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface vs.
the one-to-one verbose tools.

## Tools & actions
Prefer the **condensed** tool; `action` + a `params_json` **JSON string**.

| Condensed tool | Key actions |
|----------------|-------------|
| `mealie_households` | `get_households_mealplans`, `post_households_mealplans`, `get_todays_meals`, `create_random_meal`, `get_households_cookbooks`, `post_households_cookbooks`, `get_households_shopping_lists`, `post_households_shopping_lists`, `add_recipe_ingredients_to_list`, `get_households_shopping_items`, `get_household_members`, `get_statistics` |

### Key parameters
- `data` — body for creates. A meal-plan entry needs `{"date":"YYYY-MM-DD",
  "entryType":"dinner","recipeId":"<uuid>"}`.
- `item_id` — the cookbook / shopping-list / meal-plan id for get/put/delete.
- `start_date` / `end_date` — range filters on `get_households_mealplans`.

## Recipes (`params_json`)
Read this week's meal plan:
```json
{"start_date":"2026-07-01","end_date":"2026-07-07"}
```
Schedule a recipe for a date:
```json
{"data":{"date":"2026-07-05","entryType":"dinner","recipeId":"<recipe-uuid>"}}
```
Seed a shopping list from a recipe's ingredients:
```json
{"item_id":"<shopping-list-uuid>","data":{"recipeId":"<recipe-uuid>","recipeIncrementQuantity":1}}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object.
- Meal plans, cookbooks and shopping lists are **household-scoped** — they live
  under the token user's household; there is no cross-household write here (use
  `mealie_explore` for read-only cross-group access).
- Meal-plan `entryType` is a choice (`breakfast`/`lunch`/`dinner`/`side`); `date`
  is `YYYY-MM-DD`.
- A meal-plan entry references a recipe by its **UUID `recipeId`**, not its slug —
  resolve the id via `mealie_recipes` `get_recipes` first.
- Cookbooks are **filter definitions** (categories/tags/tools), not static lists;
  their membership is computed from the recipe catalog.

## Related
- `mealie-recipe-management` supplies the recipes scheduled and shopped here.
- `mealie-organizer-catalog` defines the categories/tags a cookbook filters on.
