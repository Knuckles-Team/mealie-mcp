---
name: mealie-organizer-operations
skill_type: skill
description: >-
  Maintain recipe categories, tags and tools. Do NOT use for tasks outside the mealie-mcp
  connector.
license: MIT
tags: [mealie, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Mealie categories, tags and tools

Use the typed tools of the `mealie-mcp` connector: one tool per upstream API operation, named `mealie_<operation>`. Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Where the data lives

- **mealie-recipes** (`MEALIE_BASE_URL`): holds Recipe; read with `mealie_get_recipes`.
- **mealie-mealplans** (`MEALIE_BASE_URL`): holds MealPlan; read with `mealie_get_households_mealplans`.
- **mealie-shopping** (`MEALIE_BASE_URL`): holds ShoppingList; read with `mealie_get_households_shopping_lists`.
- **mealie-cookbooks** (`MEALIE_BASE_URL`): holds Cookbook; read with `mealie_get_households_cookbooks`.
- **mealie-categories** (`MEALIE_BASE_URL`): holds RecipeCategory; read with `mealie_get_organizers_categories`.
- **mealie-foods** (`MEALIE_BASE_URL`): holds Food; read with `mealie_get_foods`.
- **mealie-households** (`MEALIE_BASE_URL`): holds Household; read with `mealie_get_all_households`.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology. Run the steps in order; read before you write.

### `mealie-manage-category`

1. `mealie_get_organizers_categories` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`, `search`) - Get organizers categories.
2. `mealie_get_organizers_categories_item_id` (`accept_language`, `item_id`) - Get organizers categories item id.
3. `mealie_get_organizers_categories_slug_category_slug` (`accept_language`, `category_slug`) - Get organizers categories slug category slug.
4. `mealie_post_organizers_categories` (`accept_language`, `data`) - Post organizers categories.
5. `mealie_put_organizers_categories_item_id` (`accept_language`, `data`, `item_id`) - Put organizers categories item id.
6. `mealie_delete_organizers_categories_item_id` (`accept_language`, `confirm`, `item_id`) - Delete organizers categories item id. (destructive: ask the operator first)

### `mealie-manage-tool`

1. `mealie_get_organizers_tools` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`, `search`) - Get organizers tools.
2. `mealie_get_organizers_tools_item_id` (`accept_language`, `item_id`) - Get organizers tools item id.
3. `mealie_get_organizers_tools_slug_tool_slug` (`accept_language`, `tool_slug`) - Get organizers tools slug tool slug.
4. `mealie_post_organizers_tools` (`accept_language`, `data`) - Post organizers tools.
5. `mealie_put_organizers_tools_item_id` (`accept_language`, `data`, `item_id`) - Put organizers tools item id.
6. `mealie_delete_organizers_tools_item_id` (`accept_language`, `confirm`, `item_id`) - Delete organizers tools item id. (destructive: ask the operator first)

### `mealie-manage-tag`

1. `mealie_get_empty_tags` (`accept_language`) - Get empty tags.
2. `mealie_get_organizers_tags` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`, `search`) - Get organizers tags.
3. `mealie_get_organizers_tags_item_id` (`accept_language`, `item_id`) - Get organizers tags item id.
4. `mealie_get_organizers_tags_slug_tag_slug` (`accept_language`, `tag_slug`) - Get organizers tags slug tag slug.
5. `mealie_post_organizers_tags` (`accept_language`, `data`) - Post organizers tags.
6. `mealie_put_organizers_tags_item_id` (`accept_language`, `data`, `item_id`) - Put organizers tags item id.
7. `mealie_delete_recipe_tag` (`accept_language`, `confirm`, `item_id`) - Delete recipe tag. (destructive: ask the operator first)

### `mealie-inspect-organizer`

1. `mealie_get_all_empty` (`accept_language`) - Get all empty.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the Mealie API token or users' credentials.
- Identify recipes by slug and other records by id; confirm the record exists before changing or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
