---
name: mealie-server-administration
skill_type: skill
description: >-
  Administer the server: backups, maintenance, group and household administration and
  configuration checks. Do NOT use for tasks outside the mealie-mcp connector.
license: MIT
tags: [mealie, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Mealie server administration

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

### `mealie-manage-app`

1. `mealie_check_app_config` (`accept_language`) - Check app config.
2. `mealie_check_email_config` (`accept_language`) - Check email config.
3. `mealie_get_app_info` (`accept_language`) - Get app info.
4. `mealie_get_app_statistics` (`accept_language`) - Get app statistics.
5. `mealie_get_app_theme` (no parameters) - Get app theme.
6. `mealie_get_startup_info` (no parameters) - Get startup info.
7. `mealie_get_validation_text` (no parameters) - Get validation text.
8. `mealie_send_test_email` (`accept_language`, `data`) - Send test email.
9. `mealie_debug_openai` (`accept_language`, `data`) - Run debug openai.

### `mealie-manage-maintenance`

1. `mealie_get_maintenance_summary` (`accept_language`) - Get maintenance summary.
2. `mealie_get_storage` (`accept_language`) - Get storage.
3. `mealie_get_storage_details` (`accept_language`) - Get storage details.
4. `mealie_clean_images` (`accept_language`) - Run clean images. (destructive: ask the operator first)
5. `mealie_clean_recipe_folders` (`accept_language`) - Run clean recipe folders. (destructive: ask the operator first)
6. `mealie_clean_temp` (`accept_language`) - Run clean temp. (destructive: ask the operator first)

### `mealie-manage-backup`

1. `mealie_get_admin_backups` (`accept_language`) - Get admin backups.
2. `mealie_get_admin_backups_file_name` (`accept_language`, `file_name`) - Get admin backups file name.
3. `mealie_get_exported_data` (`accept_language`) - Get exported data.
4. `mealie_get_exported_data_token` (`accept_language`, `export_id`) - Get exported data token.
5. `mealie_post_admin_backups` (`accept_language`) - Post admin backups.
6. `mealie_download_file` (`token`) - Download file.
7. `mealie_delete_admin_backups_file_name` (`accept_language`, `confirm`, `file_name`) - Delete admin backups file name. (destructive: ask the operator first)
8. `mealie_purge_export_data` (`accept_language`, `confirm`) - Purge export data. (destructive: ask the operator first)

### `mealie-manage-group-admin`

1. `mealie_get_admin_groups` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`) - Get admin groups.
2. `mealie_get_admin_groups_item_id` (`accept_language`, `item_id`) - Get admin groups item id.
3. `mealie_get_admin_households` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`) - Get admin households.
4. `mealie_get_admin_households_item_id` (`accept_language`, `item_id`) - Get admin households item id.
5. `mealie_get_all_households` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`) - Get all households.
6. `mealie_post_admin_groups` (`accept_language`, `data`) - Post admin groups.
7. `mealie_post_admin_households` (`accept_language`, `data`) - Post admin households.
8. `mealie_put_admin_groups_item_id` (`accept_language`, `data`, `item_id`) - Put admin groups item id.
9. `mealie_put_admin_households_item_id` (`accept_language`, `data`, `item_id`) - Put admin households item id.
10. `mealie_delete_admin_groups_item_id` (`accept_language`, `confirm`, `item_id`) - Delete admin groups item id. (destructive: ask the operator first)
11. `mealie_delete_admin_households_item_id` (`accept_language`, `confirm`, `item_id`) - Delete admin households item id. (destructive: ask the operator first)

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the Mealie API token or users' credentials.
- Identify recipes by slug and other records by id; confirm the record exists before changing or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
