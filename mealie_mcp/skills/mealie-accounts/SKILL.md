---
name: mealie-accounts
skill_type: skill
description: >-
  Sign in, manage the current user and their favorites and ratings, and administer user
  accounts. Do NOT use for tasks outside the mealie-mcp connector.
license: MIT
tags: [mealie, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Mealie accounts and sign-in

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

### `mealie-manage-rating`

1. `mealie_get_favorites` (`accept_language`, `id`) - Get favorites.
2. `mealie_get_logged_in_user_favorites` (`accept_language`) - Get logged in user favorites.
3. `mealie_get_logged_in_user_rating_for_recipe` (`accept_language`, `recipe_id`) - Get logged in user rating for recipe.
4. `mealie_get_logged_in_user_ratings` (`accept_language`) - Get logged in user ratings.
5. `mealie_get_ratings` (`accept_language`, `id`) - Get ratings.
6. `mealie_add_favorite` (`accept_language`, `id`, `slug`) - Add favorite.
7. `mealie_set_rating` (`accept_language`, `data`, `id`, `slug`) - Set rating.
8. `mealie_remove_favorite` (`accept_language`, `confirm`, `id`, `slug`) - Remove favorite. (destructive: ask the operator first)

### `mealie-manage-profile`

1. `mealie_get_logged_in_user` (`accept_language`) - Get logged in user.
2. `mealie_get_user_image` (`file_name`, `user_id`) - Get user image.
3. `mealie_create` (`accept_language`, `data`) - Create.
4. `mealie_register_new_user` (`accept_language`, `data`) - Register new user.
5. `mealie_update_user` (`accept_language`, `data`, `item_id`) - Update user.
6. `mealie_update_user_image` (`accept_language`, `data`, `id`) - Update user image.
7. `mealie_delete` (`accept_language`, `confirm`, `token_id`) - Delete. (destructive: ask the operator first)

### `mealie-manage-admin-user`

1. `mealie_get_admin_users` (`accept_language`, `order_by`, `order_by_null_position`, `order_direction`, `page`, `pagination_seed`, `per_page`, `query_filter`) - Get admin users.
2. `mealie_get_admin_users_item_id` (`accept_language`, `item_id`) - Get admin users item id.
3. `mealie_post_admin_users` (`accept_language`, `data`) - Post admin users.
4. `mealie_put_admin_users_item_id` (`accept_language`, `data`, `item_id`) - Put admin users item id.
5. `mealie_delete_admin_users_item_id` (`accept_language`, `confirm`, `item_id`) - Delete admin users item id. (destructive: ask the operator first)

### `mealie-manage-auth`

1. `mealie_get_token` (`data`) - Get token.
2. `mealie_forgot_password` (`accept_language`, `data`) - Run forgot password.
3. `mealie_generate_token` (`accept_language`, `data`) - Run generate token.
4. `mealie_logout` (`accept_language`) - Run logout.
5. `mealie_oauth_callback` (no parameters) - Run oauth callback.
6. `mealie_oauth_login` (no parameters) - Run oauth login.
7. `mealie_refresh_token` (no parameters) - Run refresh token.
8. `mealie_update_password` (`accept_language`, `data`) - Update password.
9. `mealie_reset_password` (`data`) - Reset password. (destructive: ask the operator first)

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the Mealie API token or users' credentials.
- Identify recipes by slug and other records by id; confirm the record exists before changing or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
