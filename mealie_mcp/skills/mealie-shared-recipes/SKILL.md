---
name: mealie-shared-recipes
skill_type: skill
description: >-
  Share recipes by link and read shared recipes. Do NOT use for tasks outside the
  mealie-mcp connector.
license: MIT
tags: [mealie, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Mealie shared recipes

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

### `mealie-manage-shared-recipe`

1. `mealie_get_shared_recipe` (`token_id`) - Get shared recipe.
2. `mealie_get_shared_recipe_as_zip` (`token_id`) - Get shared recipe as zip.
3. `mealie_get_shared_recipes` (`accept_language`, `recipe_id`) - Get shared recipes.
4. `mealie_get_shared_recipes_item_id` (`accept_language`, `item_id`) - Get shared recipes item id.
5. `mealie_post_shared_recipes` (`accept_language`, `data`) - Post shared recipes.
6. `mealie_delete_shared_recipes_item_id` (`accept_language`, `confirm`, `item_id`) - Delete shared recipes item id. (destructive: ask the operator first)

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the Mealie API token or users' credentials.
- Identify recipes by slug and other records by id; confirm the record exists before changing or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
