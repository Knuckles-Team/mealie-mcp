---
name: mealie-foods-and-units
skill_type: skill
description: >-
  Maintain foods and units and parse free-text ingredients. Do NOT use for tasks outside
  the mealie-mcp connector.
license: MIT
tags: [mealie, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Mealie foods, units and ingredient parsing

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

### `mealie-manage-food`

1. `mealie_get_foods` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`, `search`) - Get foods.
2. `mealie_get_foods_item_id` (`accept_language`, `item_id`) - Get foods item id.
3. `mealie_post_foods` (`accept_language`, `data`) - Post foods.
4. `mealie_recipe_food_create` (`data`) - Run recipe food create.
5. `mealie_put_foods_item_id` (`accept_language`, `data`, `item_id`) - Put foods item id.
6. `mealie_recipe_foods` (`page`, `per_page`, `search`) - Run recipe foods.
7. `mealie_seed_foods` (`accept_language`, `data`) - Run seed foods.
8. `mealie_delete_foods_item_id` (`accept_language`, `confirm`, `item_id`) - Delete foods item id. (destructive: ask the operator first)
9. `mealie_put_foods_merge` (`accept_language`, `data`) - Put foods merge. (destructive: ask the operator first)

### `mealie-manage-unit`

1. `mealie_get_units` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`, `search`) - Get units.
2. `mealie_get_units_item_id` (`accept_language`, `item_id`) - Get units item id.
3. `mealie_post_units` (`accept_language`, `data`) - Post units.
4. `mealie_recipe_unit_create` (`data`) - Run recipe unit create.
5. `mealie_put_units_item_id` (`accept_language`, `data`, `item_id`) - Put units item id.
6. `mealie_recipe_units` (`page`, `per_page`, `search`) - Run recipe units.
7. `mealie_seed_units` (`accept_language`, `data`) - Run seed units.
8. `mealie_delete_units_item_id` (`accept_language`, `confirm`, `item_id`) - Delete units item id. (destructive: ask the operator first)
9. `mealie_put_units_merge` (`accept_language`, `data`) - Put units merge. (destructive: ask the operator first)

### `mealie-inspect-parser`

1. `mealie_parse_ingredient` (`accept_language`, `data`) - Run parse ingredient.
2. `mealie_parse_ingredients` (`accept_language`, `data`) - Run parse ingredients.
3. `mealie_post_parser_ingredient` (`accept_language`, `confirm`, `item_id`) - Post parser ingredient.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the Mealie API token or users' credentials.
- Identify recipes by slug and other records by id; confirm the record exists before changing or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
