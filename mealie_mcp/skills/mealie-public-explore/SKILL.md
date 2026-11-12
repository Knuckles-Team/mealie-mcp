---
name: mealie-public-explore
skill_type: skill
description: >-
  Browse a group's public recipes, organizers, foods and cookbooks without signing in. Do
  NOT use for tasks outside the mealie-mcp connector.
license: MIT
tags: [mealie, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Mealie public explore

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

### `mealie-inspect-explore-catalog`

1. `mealie_get_explore_groups_group_slug_cookbooks` (`accept_language`, `group_slug`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`, `search`) - Get explore groups group slug cookbooks.
2. `mealie_get_explore_groups_group_slug_cookbooks_item_id` (`accept_language`, `group_slug`, `item_id`) - Get explore groups group slug cookbooks item id.
3. `mealie_get_explore_groups_group_slug_foods` (`accept_language`, `group_slug`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`, `search`) - Get explore groups group slug foods.
4. `mealie_get_explore_groups_group_slug_foods_item_id` (`accept_language`, `group_slug`, `item_id`) - Get explore groups group slug foods item id.
5. `mealie_get_explore_groups_group_slug_households` (`accept_language`, `group_slug`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`) - Get explore groups group slug households.

### `mealie-inspect-explore-organizer`

1. `mealie_get_explore_groups_group_slug_organizers_categories` (`accept_language`, `group_slug`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`, `search`) - Get explore groups group slug organizers categories.
2. `mealie_get_explore_groups_group_slug_organizers_categories_item_id` (`accept_language`, `group_slug`, `item_id`) - Get explore groups group slug organizers categories item id.
3. `mealie_get_explore_groups_group_slug_organizers_tags` (`accept_language`, `group_slug`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`, `search`) - Get explore groups group slug organizers tags.
4. `mealie_get_explore_groups_group_slug_organizers_tags_item_id` (`accept_language`, `group_slug`, `item_id`) - Get explore groups group slug organizers tags item id.
5. `mealie_get_explore_groups_group_slug_organizers_tools` (`accept_language`, `group_slug`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`, `search`) - Get explore groups group slug organizers tools.
6. `mealie_get_explore_groups_group_slug_organizers_tools_item_id` (`accept_language`, `group_slug`, `item_id`) - Get explore groups group slug organizers tools item id.

### `mealie-inspect-explore-recipe`

1. `mealie_get_explore_groups_group_slug_recipes` (`accept_language`, `categories`, `cookbook`, `foods`, `group_slug`, `households`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`, `require_all_categories`, `require_all_foods`, `require_all_tags`, `require_all_tools`, `search`, `tags`, `tools`) - Get explore groups group slug recipes.
2. `mealie_get_explore_groups_group_slug_recipes_suggestions` (`accept_language`, `foods`, `group_slug`, `include_foods_on_hand`, `include_tools_on_hand`, `limit`, `max_missing_foods`, `max_missing_tools`, `order_by`, `order_by_null_position`, `order_direction`, `pagination_seed`, `query_filter`, `tools`) - Get explore groups group slug recipes suggestions.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the Mealie API token or users' credentials.
- Identify recipes by slug and other records by id; confirm the record exists before changing or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
