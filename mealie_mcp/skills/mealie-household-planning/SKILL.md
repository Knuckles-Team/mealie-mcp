---
name: mealie-household-planning
skill_type: skill
description: >-
  Plan meals, keep shopping lists, run cookbooks, webhooks and notifications, and manage
  households and groups. Do NOT use for tasks outside the mealie-mcp connector.
license: MIT
tags: [mealie, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Mealie meal plans, shopping and households

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

### `mealie-manage-shopping`

1. `mealie_get_households_shopping_items` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`) - Get households shopping items.
2. `mealie_get_households_shopping_items_item_id` (`accept_language`, `item_id`) - Get households shopping items item id.
3. `mealie_get_households_shopping_lists` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`) - Get households shopping lists.
4. `mealie_get_households_shopping_lists_item_id` (`accept_language`, `item_id`) - Get households shopping lists item id.
5. `mealie_add_recipe_ingredients_to_list` (`accept_language`, `data`, `item_id`) - Add recipe ingredients to list.
6. `mealie_add_single_recipe_ingredients_to_list` (`accept_language`, `data`, `item_id`, `recipe_id`) - Add single recipe ingredients to list.
7. `mealie_post_households_shopping_items` (`accept_language`, `data`) - Post households shopping items.
8. `mealie_post_households_shopping_items_create_bulk` (`accept_language`, `data`) - Post households shopping items create bulk.
9. `mealie_post_households_shopping_lists` (`accept_language`, `data`) - Post households shopping lists.
10. `mealie_put_households_shopping_items` (`accept_language`, `data`) - Put households shopping items.
11. `mealie_put_households_shopping_items_item_id` (`accept_language`, `data`, `item_id`) - Put households shopping items item id.
12. `mealie_put_households_shopping_lists_item_id` (`accept_language`, `data`, `item_id`) - Put households shopping lists item id.
13. `mealie_delete_households_shopping_items` (`accept_language`, `confirm`, `ids`) - Delete households shopping items. (destructive: ask the operator first)
14. `mealie_delete_households_shopping_items_item_id` (`accept_language`, `confirm`, `item_id`) - Delete households shopping items item id. (destructive: ask the operator first)
15. `mealie_delete_households_shopping_lists_item_id` (`accept_language`, `confirm`, `item_id`) - Delete households shopping lists item id. (destructive: ask the operator first)

### `mealie-manage-household`

1. `mealie_get_group_member` (`accept_language`, `username_or_id`) - Get group member.
2. `mealie_get_group_members` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`) - Get group members.
3. `mealie_get_group_preferences` (`accept_language`) - Get group preferences.
4. `mealie_get_household` (`accept_language`, `group_slug`, `household_slug`) - Get household.
5. `mealie_get_household_members` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`) - Get household members.
6. `mealie_get_household_preferences` (`accept_language`) - Get household preferences.
7. `mealie_get_household_recipe` (`accept_language`, `recipe_slug`) - Get household recipe.
8. `mealie_get_invite_tokens` (`accept_language`) - Get invite tokens.
9. `mealie_get_logged_in_user_group` (`accept_language`) - Get logged in user group.
10. `mealie_get_logged_in_user_household` (`accept_language`) - Get logged in user household.
11. `mealie_get_one_household` (`accept_language`, `household_slug`) - Get one household.
12. `mealie_get_statistics` (`accept_language`) - Get statistics.
13. `mealie_create_invite_token` (`accept_language`, `data`) - Create invite token.
14. `mealie_email_invitation` (`accept_language`, `data`) - Run email invitation.
15. `mealie_set_member_permissions` (`accept_language`, `data`) - Set member permissions.
16. `mealie_update_group_preferences` (`accept_language`, `data`) - Update group preferences.
17. `mealie_update_household_preferences` (`accept_language`, `data`) - Update household preferences.

### `mealie-manage-mealplan`

1. `mealie_get_households_mealplans` (`accept_language`, `end_date`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`, `start_date`) - Get households mealplans.
2. `mealie_get_households_mealplans_item_id` (`accept_language`, `item_id`) - Get households mealplans item id.
3. `mealie_get_households_mealplans_rules` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`) - Get households mealplans rules.
4. `mealie_get_households_mealplans_rules_item_id` (`accept_language`, `item_id`) - Get households mealplans rules item id.
5. `mealie_get_todays_meals` (`accept_language`) - Get todays meals.
6. `mealie_create_random_meal` (`accept_language`, `data`) - Create random meal.
7. `mealie_post_households_mealplans` (`accept_language`, `data`) - Post households mealplans.
8. `mealie_post_households_mealplans_rules` (`accept_language`, `data`) - Post households mealplans rules.
9. `mealie_put_households_mealplans_item_id` (`accept_language`, `data`, `item_id`) - Put households mealplans item id.
10. `mealie_put_households_mealplans_rules_item_id` (`accept_language`, `data`, `item_id`) - Put households mealplans rules item id.
11. `mealie_delete_households_mealplans_item_id` (`accept_language`, `confirm`, `item_id`) - Delete households mealplans item id. (destructive: ask the operator first)
12. `mealie_delete_households_mealplans_rules_item_id` (`accept_language`, `confirm`, `item_id`) - Delete households mealplans rules item id. (destructive: ask the operator first)

### `mealie-manage-label`

1. `mealie_get_groups_labels` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`, `search`) - Get groups labels.
2. `mealie_get_groups_labels_item_id` (`accept_language`, `item_id`) - Get groups labels item id.
3. `mealie_post_groups_labels` (`accept_language`, `data`) - Post groups labels.
4. `mealie_put_groups_labels_item_id` (`accept_language`, `data`, `item_id`) - Put groups labels item id.
5. `mealie_seed_labels` (`accept_language`, `data`) - Run seed labels.
6. `mealie_update_label_settings` (`accept_language`, `data`, `item_id`) - Update label settings.
7. `mealie_delete_groups_labels_item_id` (`accept_language`, `confirm`, `item_id`) - Delete groups labels item id. (destructive: ask the operator first)

### `mealie-manage-report`

1. `mealie_get_groups_reports` (`accept_language`, `report_type`) - Get groups reports.
2. `mealie_get_groups_reports_item_id` (`accept_language`, `item_id`) - Get groups reports item id.
3. `mealie_delete_groups_reports_item_id` (`accept_language`, `confirm`, `item_id`) - Delete groups reports item id. (destructive: ask the operator first)

### `mealie-manage-cookbook`

1. `mealie_get_households_cookbooks` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`) - Get households cookbooks.
2. `mealie_get_households_cookbooks_item_id` (`accept_language`, `item_id`) - Get households cookbooks item id.
3. `mealie_post_households_cookbooks` (`accept_language`, `data`) - Post households cookbooks.
4. `mealie_put_households_cookbooks` (`accept_language`, `data`) - Put households cookbooks.
5. `mealie_put_households_cookbooks_item_id` (`accept_language`, `data`, `item_id`) - Put households cookbooks item id.
6. `mealie_delete_households_cookbooks_item_id` (`accept_language`, `confirm`, `item_id`) - Delete households cookbooks item id. (destructive: ask the operator first)

### `mealie-manage-automation`

1. `mealie_get_households_events_notifications` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`) - Get households events notifications.
2. `mealie_get_households_events_notifications_item_id` (`accept_language`, `item_id`) - Get households events notifications item id.
3. `mealie_get_households_recipe_actions` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`) - Get households recipe actions.
4. `mealie_get_households_recipe_actions_item_id` (`accept_language`, `item_id`) - Get households recipe actions item id.
5. `mealie_get_households_webhooks` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`) - Get households webhooks.
6. `mealie_get_households_webhooks_item_id` (`accept_language`, `item_id`) - Get households webhooks item id.
7. `mealie_post_households_events_notifications` (`accept_language`, `data`) - Post households events notifications.
8. `mealie_post_households_recipe_actions` (`accept_language`, `data`) - Post households recipe actions.
9. `mealie_post_households_webhooks` (`accept_language`, `data`) - Post households webhooks.
10. `mealie_put_households_events_notifications_item_id` (`accept_language`, `data`, `item_id`) - Put households events notifications item id.
11. `mealie_put_households_recipe_actions_item_id` (`accept_language`, `data`, `item_id`) - Put households recipe actions item id.
12. `mealie_put_households_webhooks_item_id` (`accept_language`, `data`, `item_id`) - Put households webhooks item id.
13. `mealie_rerun_webhooks` (`accept_language`) - Run rerun webhooks.
14. `mealie_test_notification` (`accept_language`, `item_id`) - Run test notification.
15. `mealie_test_one` (`accept_language`, `item_id`) - Run test one.
16. `mealie_trigger_action` (`accept_language`, `data`, `item_id`, `recipe_slug`) - Run trigger action.
17. `mealie_delete_households_events_notifications_item_id` (`accept_language`, `confirm`, `item_id`) - Delete households events notifications item id. (destructive: ask the operator first)
18. `mealie_delete_households_recipe_actions_item_id` (`accept_language`, `confirm`, `item_id`) - Delete households recipe actions item id. (destructive: ask the operator first)
19. `mealie_delete_households_webhooks_item_id` (`accept_language`, `confirm`, `item_id`) - Delete households webhooks item id. (destructive: ask the operator first)

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the Mealie API token or users' credentials.
- Identify recipes by slug and other records by id; confirm the record exists before changing or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
