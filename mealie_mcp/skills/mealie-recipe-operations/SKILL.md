---
name: mealie-recipe-operations
skill_type: skill
description: >-
  Create, import, edit, bulk-change and publish recipes with their images, comments and
  timeline. Do NOT use for tasks outside the mealie-mcp connector.
license: MIT
tags: [mealie, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Mealie recipes

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

### `mealie-manage-recipe-bulk`

1. `mealie_bulk_categorize_recipes` (`accept_language`, `data`) - Bulk categorize recipes.
2. `mealie_bulk_export_recipes` (`accept_language`, `data`) - Bulk export recipes.
3. `mealie_bulk_settings_recipes` (`accept_language`, `data`) - Bulk settings recipes.
4. `mealie_bulk_tag_recipes` (`accept_language`, `data`) - Bulk tag recipes.
5. `mealie_bulk_delete_recipes` (`accept_language`, `confirm`, `data`) - Bulk delete recipes. (destructive: ask the operator first)

### `mealie-manage-recipe-import`

1. `mealie_parse_recipe_url` (`accept_language`, `data`) - Run parse recipe url.
2. `mealie_parse_recipe_url_bulk` (`accept_language`, `data`) - Run parse recipe url bulk.
3. `mealie_test_parse_recipe_url` (`accept_language`, `data`) - Run test parse recipe url.
4. `mealie_create_recipe_from_html_or_json` (`accept_language`, `data`) - Create recipe from html or json.
5. `mealie_create_recipe_from_image` (`accept_language`, `data`, `translate_language`) - Create recipe from image.
6. `mealie_create_recipe_from_zip` (`accept_language`, `data`) - Create recipe from zip.
7. `mealie_upload_one` (`accept_language`, `data`) - Upload one.
8. `mealie_import_one` (`accept_language`, `file_name`) - Run import one.
9. `mealie_ingest_recipes` (`ingest_images`, `params_json`) - Ingest recipes.
10. `mealie_scrape_image_url` (`accept_language`, `data`, `slug`) - Run scrape image url.
11. `mealie_start_data_migration` (`accept_language`, `data`) - Start data migration. (destructive: ask the operator first)

### `mealie-manage-recipe-media`

1. `mealie_get_recipe_as_format` (`accept_language`, `slug`, `template_name`) - Get recipe as format.
2. `mealie_get_recipe_asset` (`file_name`, `recipe_id`) - Get recipe asset.
3. `mealie_get_recipe_formats_and_templates` (`accept_language`) - Get recipe formats and templates.
4. `mealie_get_recipe_img` (`file_name`, `recipe_id`) - Get recipe img.
5. `mealie_get_recipe_timeline_event_img` (`file_name`, `recipe_id`, `timeline_event_id`) - Get recipe timeline event img.
6. `mealie_upload_recipe_asset` (`accept_language`, `data`, `slug`) - Upload recipe asset.
7. `mealie_update_event_image` (`accept_language`, `data`, `item_id`) - Update event image.
8. `mealie_update_recipe_image` (`accept_language`, `data`, `slug`) - Update recipe image.
9. `mealie_delete_recipe_image` (`accept_language`, `confirm`, `slug`) - Delete recipe image. (destructive: ask the operator first)

### `mealie-manage-recipe`

1. `mealie_get_recipe` (`accept_language`, `group_slug`, `recipe_slug`) - Get recipe.
2. `mealie_get_recipes` (`accept_language`, `categories`, `cookbook`, `foods`, `households`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`, `require_all_categories`, `require_all_foods`, `require_all_tags`, `require_all_tools`, `search`, `tags`, `tools`) - Get recipes.
3. `mealie_get_recipes_slug` (`accept_language`, `slug`) - Get recipes slug.
4. `mealie_get_recipes_suggestions` (`accept_language`, `foods`, `include_foods_on_hand`, `include_tools_on_hand`, `limit`, `max_missing_foods`, `max_missing_tools`, `order_by`, `order_by_null_position`, `order_direction`, `pagination_seed`, `query_filter`, `tools`) - Get recipes suggestions.
5. `mealie_post_recipes` (`accept_language`, `data`) - Post recipes.
6. `mealie_recipe_create` (`data`) - Run recipe create.
7. `mealie_duplicate_one` (`accept_language`, `data`, `slug`) - Run duplicate one.
8. `mealie_patch_many` (`accept_language`, `data`) - Patch many.
9. `mealie_patch_one` (`accept_language`, `data`, `slug`) - Patch one.
10. `mealie_put_recipes` (`accept_language`, `data`) - Put recipes.
11. `mealie_put_recipes_slug` (`accept_language`, `data`, `slug`) - Put recipes slug.
12. `mealie_recipe_patch` (`data`, `slug`) - Run recipe patch.
13. `mealie_recipe_update` (`data`, `slug`) - Run recipe update.
14. `mealie_update_last_made` (`accept_language`, `data`, `slug`) - Update last made.
15. `mealie_delete_recipes_slug` (`accept_language`, `confirm`, `slug`) - Delete recipes slug. (destructive: ask the operator first)
16. `mealie_remove_recipe_ingredients_from_list` (`accept_language`, `confirm`, `data`, `item_id`, `recipe_id`) - Remove recipe ingredients from list. (destructive: ask the operator first)
17. `mealie_unlock_users` (`accept_language`, `force`) - Run unlock users. (destructive: ask the operator first)

### `mealie-manage-recipe-timeline`

1. `mealie_get_recipes_timeline_events` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`) - Get recipes timeline events.
2. `mealie_get_recipes_timeline_events_item_id` (`accept_language`, `item_id`) - Get recipes timeline events item id.
3. `mealie_post_recipes_timeline_events` (`accept_language`, `data`) - Post recipes timeline events.
4. `mealie_put_recipes_timeline_events_item_id` (`accept_language`, `data`, `item_id`) - Put recipes timeline events item id.
5. `mealie_delete_recipes_timeline_events_item_id` (`accept_language`, `confirm`, `item_id`) - Delete recipes timeline events item id. (destructive: ask the operator first)

### `mealie-manage-recipe-comment`

1. `mealie_get_comments` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`) - Get comments.
2. `mealie_get_comments_item_id` (`accept_language`, `item_id`) - Get comments item id.
3. `mealie_get_recipe_comments` (`accept_language`, `slug`) - Get recipe comments.
4. `mealie_post_comments` (`accept_language`, `data`) - Post comments.
5. `mealie_put_comments_item_id` (`accept_language`, `data`, `item_id`) - Put comments item id.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the Mealie API token or users' credentials.
- Identify recipes by slug and other records by id; confirm the record exists before changing or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
