# Mealie```
 nightly
```
```
OAS 3.1
```

[ /openapi.json](https://demo.mealie.io/openapi.json)
Mealie is a web application for managing your recipes, meal plans, and shopping lists. This is the Restful API interactive documentation that can be used to explore the API. If you're justing getting started with the API and want to get started quickly, you can use the [API Usage | Mealie Docs](https://docs.mealie.io/documentation/getting-started/api-usage/) as a reference for how to get started.
If you have any questions or comments about mealie, please use the discord server to talk to the developers or other community members. If you'd like to file an issue, please use the [GitHub Issue Tracker | Mealie](https://github.com/mealie-recipes/mealie/issues/new/choose)
## Helpful Links
  * [Home Page](https://mealie.io)
  * [Documentation](https://docs.mealie.io)
  * [Discord](https://discord.gg/QuStdQGSGK)
  * [Demo](https://demo.mealie.io)


Authorize
### [App: About](https://demo.mealie.io/docs#/App:%20About)
GET
[/api/app/about](https://demo.mealie.io/docs#/App:%20About/get_app_info_api_app_about_get)
Get App Info
GET
[/api/app/about/startup-info](https://demo.mealie.io/docs#/App:%20About/get_startup_info_api_app_about_startup_info_get)
Get Startup Info
GET
[/api/app/about/theme](https://demo.mealie.io/docs#/App:%20About/get_app_theme_api_app_about_theme_get)
Get App Theme
### [Users: Authentication](https://demo.mealie.io/docs#/Users:%20Authentication)
POST
[/api/auth/token](https://demo.mealie.io/docs#/Users:%20Authentication/get_token_api_auth_token_post)
Get Token
GET
[/api/auth/oauth](https://demo.mealie.io/docs#/Users:%20Authentication/oauth_login_api_auth_oauth_get)
Oauth Login
GET
[/api/auth/oauth/callback](https://demo.mealie.io/docs#/Users:%20Authentication/oauth_callback_api_auth_oauth_callback_get)
Oauth Callback
GET
[/api/auth/refresh](https://demo.mealie.io/docs#/Users:%20Authentication/refresh_token_api_auth_refresh_get)
Refresh Token
POST
[/api/auth/logout](https://demo.mealie.io/docs#/Users:%20Authentication/logout_api_auth_logout_post)
Logout
### [Users: Registration](https://demo.mealie.io/docs#/Users:%20Registration)
POST
[/api/users/register](https://demo.mealie.io/docs#/Users:%20Registration/register_new_user_api_users_register_post)
Register New User
### [Users: CRUD](https://demo.mealie.io/docs#/Users:%20CRUD)
GET
[/api/users/self](https://demo.mealie.io/docs#/Users:%20CRUD/get_logged_in_user_api_users_self_get)
Get Logged In User
GET
[/api/users/self/ratings](https://demo.mealie.io/docs#/Users:%20CRUD/get_logged_in_user_ratings_api_users_self_ratings_get)
Get Logged In User Ratings
GET
[/api/users/self/ratings/{recipe_id}](https://demo.mealie.io/docs#/Users:%20CRUD/get_logged_in_user_rating_for_recipe_api_users_self_ratings__recipe_id__get)
Get Logged In User Rating For Recipe
GET
[/api/users/self/favorites](https://demo.mealie.io/docs#/Users:%20CRUD/get_logged_in_user_favorites_api_users_self_favorites_get)
Get Logged In User Favorites
PUT
[/api/users/password](https://demo.mealie.io/docs#/Users:%20CRUD/update_password_api_users_password_put)
Update Password
PUT
[/api/users/{item_id}](https://demo.mealie.io/docs#/Users:%20CRUD/update_user_api_users__item_id__put)
Update User
### [Users: Passwords](https://demo.mealie.io/docs#/Users:%20Passwords)
POST
[/api/users/forgot-password](https://demo.mealie.io/docs#/Users:%20Passwords/forgot_password_api_users_forgot_password_post)
Forgot Password
POST
[/api/users/reset-password](https://demo.mealie.io/docs#/Users:%20Passwords/reset_password_api_users_reset_password_post)
Reset Password
### [Users: Images](https://demo.mealie.io/docs#/Users:%20Images)
POST
[/api/users/{id}/image](https://demo.mealie.io/docs#/Users:%20Images/update_user_image_api_users__id__image_post)
Update User Image
### [Users: Tokens](https://demo.mealie.io/docs#/Users:%20Tokens)
POST
[/api/users/api-tokens](https://demo.mealie.io/docs#/Users:%20Tokens/create_api_token_api_users_api_tokens_post)
Create Api Token
DELETE
[/api/users/api-tokens/{token_id}](https://demo.mealie.io/docs#/Users:%20Tokens/delete_api_token_api_users_api_tokens__token_id__delete)
Delete Api Token
### [Users: Ratings](https://demo.mealie.io/docs#/Users:%20Ratings)
GET
[/api/users/{id}/ratings](https://demo.mealie.io/docs#/Users:%20Ratings/get_ratings_api_users__id__ratings_get)
Get Ratings
GET
[/api/users/{id}/favorites](https://demo.mealie.io/docs#/Users:%20Ratings/get_favorites_api_users__id__favorites_get)
Get Favorites
POST
[/api/users/{id}/ratings/{slug}](https://demo.mealie.io/docs#/Users:%20Ratings/set_rating_api_users__id__ratings__slug__post)
Set Rating
POST
[/api/users/{id}/favorites/{slug}](https://demo.mealie.io/docs#/Users:%20Ratings/add_favorite_api_users__id__favorites__slug__post)
Add Favorite
DELETE
[/api/users/{id}/favorites/{slug}](https://demo.mealie.io/docs#/Users:%20Ratings/remove_favorite_api_users__id__favorites__slug__delete)
Remove Favorite
### [Households: Cookbooks](https://demo.mealie.io/docs#/Households:%20Cookbooks)
GET
[/api/households/cookbooks](https://demo.mealie.io/docs#/Households:%20Cookbooks/get_all_api_households_cookbooks_get)
Get All
POST
[/api/households/cookbooks](https://demo.mealie.io/docs#/Households:%20Cookbooks/create_one_api_households_cookbooks_post)
Create One
PUT
[/api/households/cookbooks](https://demo.mealie.io/docs#/Households:%20Cookbooks/update_many_api_households_cookbooks_put)
Update Many
GET
[/api/households/cookbooks/{item_id}](https://demo.mealie.io/docs#/Households:%20Cookbooks/get_one_api_households_cookbooks__item_id__get)
Get One
PUT
[/api/households/cookbooks/{item_id}](https://demo.mealie.io/docs#/Households:%20Cookbooks/update_one_api_households_cookbooks__item_id__put)
Update One
DELETE
[/api/households/cookbooks/{item_id}](https://demo.mealie.io/docs#/Households:%20Cookbooks/delete_one_api_households_cookbooks__item_id__delete)
Delete One
### [Households: Event Notifications](https://demo.mealie.io/docs#/Households:%20Event%20Notifications)
GET
[/api/households/events/notifications](https://demo.mealie.io/docs#/Households:%20Event%20Notifications/get_all_api_households_events_notifications_get)
Get All
POST
[/api/households/events/notifications](https://demo.mealie.io/docs#/Households:%20Event%20Notifications/create_one_api_households_events_notifications_post)
Create One
GET
[/api/households/events/notifications/{item_id}](https://demo.mealie.io/docs#/Households:%20Event%20Notifications/get_one_api_households_events_notifications__item_id__get)
Get One
PUT
[/api/households/events/notifications/{item_id}](https://demo.mealie.io/docs#/Households:%20Event%20Notifications/update_one_api_households_events_notifications__item_id__put)
Update One
DELETE
[/api/households/events/notifications/{item_id}](https://demo.mealie.io/docs#/Households:%20Event%20Notifications/delete_one_api_households_events_notifications__item_id__delete)
Delete One
POST
[/api/households/events/notifications/{item_id}/test](https://demo.mealie.io/docs#/Households:%20Event%20Notifications/test_notification_api_households_events_notifications__item_id__test_post)
Test Notification
### [Households: Recipe Actions](https://demo.mealie.io/docs#/Households:%20Recipe%20Actions)
GET
[/api/households/recipe-actions](https://demo.mealie.io/docs#/Households:%20Recipe%20Actions/get_all_api_households_recipe_actions_get)
Get All
POST
[/api/households/recipe-actions](https://demo.mealie.io/docs#/Households:%20Recipe%20Actions/create_one_api_households_recipe_actions_post)
Create One
GET
[/api/households/recipe-actions/{item_id}](https://demo.mealie.io/docs#/Households:%20Recipe%20Actions/get_one_api_households_recipe_actions__item_id__get)
Get One
PUT
[/api/households/recipe-actions/{item_id}](https://demo.mealie.io/docs#/Households:%20Recipe%20Actions/update_one_api_households_recipe_actions__item_id__put)
Update One
DELETE
[/api/households/recipe-actions/{item_id}](https://demo.mealie.io/docs#/Households:%20Recipe%20Actions/delete_one_api_households_recipe_actions__item_id__delete)
Delete One
POST
[/api/households/recipe-actions/{item_id}/trigger/{recipe_slug}](https://demo.mealie.io/docs#/Households:%20Recipe%20Actions/trigger_action_api_households_recipe_actions__item_id__trigger__recipe_slug__post)
Trigger Action
### [Households: Self Service](https://demo.mealie.io/docs#/Households:%20Self%20Service)
GET
[/api/households/self](https://demo.mealie.io/docs#/Households:%20Self%20Service/get_logged_in_user_household_api_households_self_get)
Get Logged In User Household
GET
[/api/households/self/recipes/{recipe_slug}](https://demo.mealie.io/docs#/Households:%20Self%20Service/get_household_recipe_api_households_self_recipes__recipe_slug__get)
Get Household Recipe
GET
[/api/households/members](https://demo.mealie.io/docs#/Households:%20Self%20Service/get_household_members_api_households_members_get)
Get Household Members
GET
[/api/households/preferences](https://demo.mealie.io/docs#/Households:%20Self%20Service/get_household_preferences_api_households_preferences_get)
Get Household Preferences
PUT
[/api/households/preferences](https://demo.mealie.io/docs#/Households:%20Self%20Service/update_household_preferences_api_households_preferences_put)
Update Household Preferences
PUT
[/api/households/permissions](https://demo.mealie.io/docs#/Households:%20Self%20Service/set_member_permissions_api_households_permissions_put)
Set Member Permissions
GET
[/api/households/statistics](https://demo.mealie.io/docs#/Households:%20Self%20Service/get_statistics_api_households_statistics_get)
Get Statistics
### [Households: Invitations](https://demo.mealie.io/docs#/Households:%20Invitations)
GET
[/api/households/invitations](https://demo.mealie.io/docs#/Households:%20Invitations/get_invite_tokens_api_households_invitations_get)
Get Invite Tokens
POST
[/api/households/invitations](https://demo.mealie.io/docs#/Households:%20Invitations/create_invite_token_api_households_invitations_post)
Create Invite Token
POST
[/api/households/invitations/email](https://demo.mealie.io/docs#/Households:%20Invitations/email_invitation_api_households_invitations_email_post)
Email Invitation
### [Households: Shopping Lists](https://demo.mealie.io/docs#/Households:%20Shopping%20Lists)
GET
[/api/households/shopping/lists](https://demo.mealie.io/docs#/Households:%20Shopping%20Lists/get_all_api_households_shopping_lists_get)
Get All
POST
[/api/households/shopping/lists](https://demo.mealie.io/docs#/Households:%20Shopping%20Lists/create_one_api_households_shopping_lists_post)
Create One
GET
[/api/households/shopping/lists/{item_id}](https://demo.mealie.io/docs#/Households:%20Shopping%20Lists/get_one_api_households_shopping_lists__item_id__get)
Get One
PUT
[/api/households/shopping/lists/{item_id}](https://demo.mealie.io/docs#/Households:%20Shopping%20Lists/update_one_api_households_shopping_lists__item_id__put)
Update One
DELETE
[/api/households/shopping/lists/{item_id}](https://demo.mealie.io/docs#/Households:%20Shopping%20Lists/delete_one_api_households_shopping_lists__item_id__delete)
Delete One
PUT
[/api/households/shopping/lists/{item_id}/label-settings](https://demo.mealie.io/docs#/Households:%20Shopping%20Lists/update_label_settings_api_households_shopping_lists__item_id__label_settings_put)
Update Label Settings
POST
[/api/households/shopping/lists/{item_id}/recipe](https://demo.mealie.io/docs#/Households:%20Shopping%20Lists/add_recipe_ingredients_to_list_api_households_shopping_lists__item_id__recipe_post)
Add Recipe Ingredients To List
POST
[/api/households/shopping/lists/{item_id}/recipe/{recipe_id}](https://demo.mealie.io/docs#/Households:%20Shopping%20Lists/add_single_recipe_ingredients_to_list_api_households_shopping_lists__item_id__recipe__recipe_id__post)
Add Single Recipe Ingredients To List
POST
[/api/households/shopping/lists/{item_id}/recipe/{recipe_id}/delete](https://demo.mealie.io/docs#/Households:%20Shopping%20Lists/remove_recipe_ingredients_from_list_api_households_shopping_lists__item_id__recipe__recipe_id__delete_post)
Remove Recipe Ingredients From List
### [Households: Shopping List Items](https://demo.mealie.io/docs#/Households:%20Shopping%20List%20Items)
GET
[/api/households/shopping/items](https://demo.mealie.io/docs#/Households:%20Shopping%20List%20Items/get_all_api_households_shopping_items_get)
Get All
POST
[/api/households/shopping/items](https://demo.mealie.io/docs#/Households:%20Shopping%20List%20Items/create_one_api_households_shopping_items_post)
Create One
PUT
[/api/households/shopping/items](https://demo.mealie.io/docs#/Households:%20Shopping%20List%20Items/update_many_api_households_shopping_items_put)
Update Many
DELETE
[/api/households/shopping/items](https://demo.mealie.io/docs#/Households:%20Shopping%20List%20Items/delete_many_api_households_shopping_items_delete)
Delete Many
POST
[/api/households/shopping/items/create-bulk](https://demo.mealie.io/docs#/Households:%20Shopping%20List%20Items/create_many_api_households_shopping_items_create_bulk_post)
Create Many
GET
[/api/households/shopping/items/{item_id}](https://demo.mealie.io/docs#/Households:%20Shopping%20List%20Items/get_one_api_households_shopping_items__item_id__get)
Get One
PUT
[/api/households/shopping/items/{item_id}](https://demo.mealie.io/docs#/Households:%20Shopping%20List%20Items/update_one_api_households_shopping_items__item_id__put)
Update One
DELETE
[/api/households/shopping/items/{item_id}](https://demo.mealie.io/docs#/Households:%20Shopping%20List%20Items/delete_one_api_households_shopping_items__item_id__delete)
Delete One
### [Households: Webhooks](https://demo.mealie.io/docs#/Households:%20Webhooks)
GET
[/api/households/webhooks](https://demo.mealie.io/docs#/Households:%20Webhooks/get_all_api_households_webhooks_get)
Get All
POST
[/api/households/webhooks](https://demo.mealie.io/docs#/Households:%20Webhooks/create_one_api_households_webhooks_post)
Create One
POST
[/api/households/webhooks/rerun](https://demo.mealie.io/docs#/Households:%20Webhooks/rerun_webhooks_api_households_webhooks_rerun_post)
Rerun Webhooks
GET
[/api/households/webhooks/{item_id}](https://demo.mealie.io/docs#/Households:%20Webhooks/get_one_api_households_webhooks__item_id__get)
Get One
PUT
[/api/households/webhooks/{item_id}](https://demo.mealie.io/docs#/Households:%20Webhooks/update_one_api_households_webhooks__item_id__put)
Update One
DELETE
[/api/households/webhooks/{item_id}](https://demo.mealie.io/docs#/Households:%20Webhooks/delete_one_api_households_webhooks__item_id__delete)
Delete One
POST
[/api/households/webhooks/{item_id}/test](https://demo.mealie.io/docs#/Households:%20Webhooks/test_one_api_households_webhooks__item_id__test_post)
Test One
### [Households: Mealplan Rules](https://demo.mealie.io/docs#/Households:%20Mealplan%20Rules)
GET
[/api/households/mealplans/rules](https://demo.mealie.io/docs#/Households:%20Mealplan%20Rules/get_all_api_households_mealplans_rules_get)
Get All
POST
[/api/households/mealplans/rules](https://demo.mealie.io/docs#/Households:%20Mealplan%20Rules/create_one_api_households_mealplans_rules_post)
Create One
GET
[/api/households/mealplans/rules/{item_id}](https://demo.mealie.io/docs#/Households:%20Mealplan%20Rules/get_one_api_households_mealplans_rules__item_id__get)
Get One
PUT
[/api/households/mealplans/rules/{item_id}](https://demo.mealie.io/docs#/Households:%20Mealplan%20Rules/update_one_api_households_mealplans_rules__item_id__put)
Update One
DELETE
[/api/households/mealplans/rules/{item_id}](https://demo.mealie.io/docs#/Households:%20Mealplan%20Rules/delete_one_api_households_mealplans_rules__item_id__delete)
Delete One
### [Households: Mealplans](https://demo.mealie.io/docs#/Households:%20Mealplans)
GET
[/api/households/mealplans](https://demo.mealie.io/docs#/Households:%20Mealplans/get_all_api_households_mealplans_get)
Get All
POST
[/api/households/mealplans](https://demo.mealie.io/docs#/Households:%20Mealplans/create_one_api_households_mealplans_post)
Create One
GET
[/api/households/mealplans/today](https://demo.mealie.io/docs#/Households:%20Mealplans/get_todays_meals_api_households_mealplans_today_get)
Get Todays Meals
POST
[/api/households/mealplans/random](https://demo.mealie.io/docs#/Households:%20Mealplans/create_random_meal_api_households_mealplans_random_post)
Create Random Meal
GET
[/api/households/mealplans/{item_id}](https://demo.mealie.io/docs#/Households:%20Mealplans/get_one_api_households_mealplans__item_id__get)
Get One
PUT
[/api/households/mealplans/{item_id}](https://demo.mealie.io/docs#/Households:%20Mealplans/update_one_api_households_mealplans__item_id__put)
Update One
DELETE
[/api/households/mealplans/{item_id}](https://demo.mealie.io/docs#/Households:%20Mealplans/delete_one_api_households_mealplans__item_id__delete)
Delete One
### [Groups: Households](https://demo.mealie.io/docs#/Groups:%20Households)
GET
[/api/groups/households](https://demo.mealie.io/docs#/Groups:%20Households/get_all_households_api_groups_households_get)
Get All Households
GET
[/api/groups/households/{household_slug}](https://demo.mealie.io/docs#/Groups:%20Households/get_one_household_api_groups_households__household_slug__get)
Get One Household
### [Groups: Self Service](https://demo.mealie.io/docs#/Groups:%20Self%20Service)
GET
[/api/groups/self](https://demo.mealie.io/docs#/Groups:%20Self%20Service/get_logged_in_user_group_api_groups_self_get)
Get Logged In User Group
GET
[/api/groups/members](https://demo.mealie.io/docs#/Groups:%20Self%20Service/get_group_members_api_groups_members_get)
Get Group Members
GET
[/api/groups/members/{username_or_id}](https://demo.mealie.io/docs#/Groups:%20Self%20Service/get_group_member_api_groups_members__username_or_id__get)
Get Group Member
GET
[/api/groups/preferences](https://demo.mealie.io/docs#/Groups:%20Self%20Service/get_group_preferences_api_groups_preferences_get)
Get Group Preferences
PUT
[/api/groups/preferences](https://demo.mealie.io/docs#/Groups:%20Self%20Service/update_group_preferences_api_groups_preferences_put)
Update Group Preferences
GET
[/api/groups/storage](https://demo.mealie.io/docs#/Groups:%20Self%20Service/get_storage_api_groups_storage_get)
Get Storage
### [Groups: Migrations](https://demo.mealie.io/docs#/Groups:%20Migrations)
POST
[/api/groups/migrations](https://demo.mealie.io/docs#/Groups:%20Migrations/start_data_migration_api_groups_migrations_post)
Start Data Migration
### [Groups: Reports](https://demo.mealie.io/docs#/Groups:%20Reports)
GET
[/api/groups/reports](https://demo.mealie.io/docs#/Groups:%20Reports/get_all_api_groups_reports_get)
Get All
GET
[/api/groups/reports/{item_id}](https://demo.mealie.io/docs#/Groups:%20Reports/get_one_api_groups_reports__item_id__get)
Get One
DELETE
[/api/groups/reports/{item_id}](https://demo.mealie.io/docs#/Groups:%20Reports/delete_one_api_groups_reports__item_id__delete)
Delete One
### [Groups: Multi Purpose Labels](https://demo.mealie.io/docs#/Groups:%20Multi%20Purpose%20Labels)
GET
[/api/groups/labels](https://demo.mealie.io/docs#/Groups:%20Multi%20Purpose%20Labels/get_all_api_groups_labels_get)
Get All
POST
[/api/groups/labels](https://demo.mealie.io/docs#/Groups:%20Multi%20Purpose%20Labels/create_one_api_groups_labels_post)
Create One
GET
[/api/groups/labels/{item_id}](https://demo.mealie.io/docs#/Groups:%20Multi%20Purpose%20Labels/get_one_api_groups_labels__item_id__get)
Get One
PUT
[/api/groups/labels/{item_id}](https://demo.mealie.io/docs#/Groups:%20Multi%20Purpose%20Labels/update_one_api_groups_labels__item_id__put)
Update One
DELETE
[/api/groups/labels/{item_id}](https://demo.mealie.io/docs#/Groups:%20Multi%20Purpose%20Labels/delete_one_api_groups_labels__item_id__delete)
Delete One
### [Groups: Seeders](https://demo.mealie.io/docs#/Groups:%20Seeders)
POST
[/api/groups/seeders/foods](https://demo.mealie.io/docs#/Groups:%20Seeders/seed_foods_api_groups_seeders_foods_post)
Seed Foods
POST
[/api/groups/seeders/labels](https://demo.mealie.io/docs#/Groups:%20Seeders/seed_labels_api_groups_seeders_labels_post)
Seed Labels
POST
[/api/groups/seeders/units](https://demo.mealie.io/docs#/Groups:%20Seeders/seed_units_api_groups_seeders_units_post)
Seed Units
### [Recipe: Exports](https://demo.mealie.io/docs#/Recipe:%20Exports)
GET
[/api/recipes/exports](https://demo.mealie.io/docs#/Recipe:%20Exports/get_recipe_formats_and_templates_api_recipes_exports_get)
Get Recipe Formats And Templates
GET
[/api/recipes/{slug}/exports](https://demo.mealie.io/docs#/Recipe:%20Exports/get_recipe_as_format_api_recipes__slug__exports_get)
Get Recipe As Format
### [Recipe: CRUD](https://demo.mealie.io/docs#/Recipe:%20CRUD)
POST
[/api/recipes/test-scrape-url](https://demo.mealie.io/docs#/Recipe:%20CRUD/test_parse_recipe_url_api_recipes_test_scrape_url_post)
Test Parse Recipe Url
POST
[/api/recipes/create/html-or-json](https://demo.mealie.io/docs#/Recipe:%20CRUD/create_recipe_from_html_or_json_api_recipes_create_html_or_json_post)
Create Recipe From Html Or Json
POST
[/api/recipes/create/url](https://demo.mealie.io/docs#/Recipe:%20CRUD/parse_recipe_url_api_recipes_create_url_post)
Parse Recipe Url
POST
[/api/recipes/create/url/bulk](https://demo.mealie.io/docs#/Recipe:%20CRUD/parse_recipe_url_bulk_api_recipes_create_url_bulk_post)
Parse Recipe Url Bulk
POST
[/api/recipes/create/zip](https://demo.mealie.io/docs#/Recipe:%20CRUD/create_recipe_from_zip_api_recipes_create_zip_post)
Create Recipe From Zip
POST
[/api/recipes/create/image](https://demo.mealie.io/docs#/Recipe:%20CRUD/create_recipe_from_image_api_recipes_create_image_post)
Create Recipe From Image
GET
[/api/recipes](https://demo.mealie.io/docs#/Recipe:%20CRUD/get_all_api_recipes_get)
Get All
POST
[/api/recipes](https://demo.mealie.io/docs#/Recipe:%20CRUD/create_one_api_recipes_post)
Create One
PUT
[/api/recipes](https://demo.mealie.io/docs#/Recipe:%20CRUD/update_many_api_recipes_put)
Update Many
PATCH
[/api/recipes](https://demo.mealie.io/docs#/Recipe:%20CRUD/patch_many_api_recipes_patch)
Patch Many
GET
[/api/recipes/suggestions](https://demo.mealie.io/docs#/Recipe:%20CRUD/suggest_recipes_api_recipes_suggestions_get)
Suggest Recipes
GET
[/api/recipes/{slug}](https://demo.mealie.io/docs#/Recipe:%20CRUD/get_one_api_recipes__slug__get)
Get One
PUT
[/api/recipes/{slug}](https://demo.mealie.io/docs#/Recipe:%20CRUD/update_one_api_recipes__slug__put)
Update One
PATCH
[/api/recipes/{slug}](https://demo.mealie.io/docs#/Recipe:%20CRUD/patch_one_api_recipes__slug__patch)
Patch One
DELETE
[/api/recipes/{slug}](https://demo.mealie.io/docs#/Recipe:%20CRUD/delete_one_api_recipes__slug__delete)
Delete One
POST
[/api/recipes/{slug}/duplicate](https://demo.mealie.io/docs#/Recipe:%20CRUD/duplicate_one_api_recipes__slug__duplicate_post)
Duplicate One
PATCH
[/api/recipes/{slug}/last-made](https://demo.mealie.io/docs#/Recipe:%20CRUD/update_last_made_api_recipes__slug__last_made_patch)
Update Last Made
POST
[/api/recipes/{slug}/image](https://demo.mealie.io/docs#/Recipe:%20CRUD/scrape_image_url_api_recipes__slug__image_post)
Scrape Image Url
PUT
[/api/recipes/{slug}/image](https://demo.mealie.io/docs#/Recipe:%20CRUD/update_recipe_image_api_recipes__slug__image_put)
Update Recipe Image
DELETE
[/api/recipes/{slug}/image](https://demo.mealie.io/docs#/Recipe:%20CRUD/delete_recipe_image_api_recipes__slug__image_delete)
Delete Recipe Image
POST
[/api/recipes/{slug}/assets](https://demo.mealie.io/docs#/Recipe:%20CRUD/upload_recipe_asset_api_recipes__slug__assets_post)
Upload Recipe Asset
### [Recipe: Images and Assets](https://demo.mealie.io/docs#/Recipe:%20Images%20and%20Assets)
POST
[/api/recipes/{slug}/image](https://demo.mealie.io/docs#/Recipe:%20Images%20and%20Assets/scrape_image_url_api_recipes__slug__image_post)
Scrape Image Url
PUT
[/api/recipes/{slug}/image](https://demo.mealie.io/docs#/Recipe:%20Images%20and%20Assets/update_recipe_image_api_recipes__slug__image_put)
Update Recipe Image
DELETE
[/api/recipes/{slug}/image](https://demo.mealie.io/docs#/Recipe:%20Images%20and%20Assets/delete_recipe_image_api_recipes__slug__image_delete)
Delete Recipe Image
POST
[/api/recipes/{slug}/assets](https://demo.mealie.io/docs#/Recipe:%20Images%20and%20Assets/upload_recipe_asset_api_recipes__slug__assets_post)
Upload Recipe Asset
GET
[/api/media/recipes/{recipe_id}/images/{file_name}](https://demo.mealie.io/docs#/Recipe:%20Images%20and%20Assets/get_recipe_img_api_media_recipes__recipe_id__images__file_name__get)
Get Recipe Img
GET
[/api/media/recipes/{recipe_id}/images/timeline/{timeline_event_id}/{file_name}](https://demo.mealie.io/docs#/Recipe:%20Images%20and%20Assets/get_recipe_timeline_event_img_api_media_recipes__recipe_id__images_timeline__timeline_event_id___file_name__get)
Get Recipe Timeline Event Img
GET
[/api/media/recipes/{recipe_id}/assets/{file_name}](https://demo.mealie.io/docs#/Recipe:%20Images%20and%20Assets/get_recipe_asset_api_media_recipes__recipe_id__assets__file_name__get)
Get Recipe Asset
GET
[/api/media/users/{user_id}/{file_name}](https://demo.mealie.io/docs#/Recipe:%20Images%20and%20Assets/get_user_image_api_media_users__user_id___file_name__get)
Get User Image
GET
[/api/media/docker/validate.txt](https://demo.mealie.io/docs#/Recipe:%20Images%20and%20Assets/get_validation_text_api_media_docker_validate_txt_get)
Get Validation Text
### [Recipe: Comments](https://demo.mealie.io/docs#/Recipe:%20Comments)
GET
[/api/recipes/{slug}/comments](https://demo.mealie.io/docs#/Recipe:%20Comments/get_recipe_comments_api_recipes__slug__comments_get)
Get Recipe Comments
GET
[/api/comments](https://demo.mealie.io/docs#/Recipe:%20Comments/get_all_api_comments_get)
Get All
POST
[/api/comments](https://demo.mealie.io/docs#/Recipe:%20Comments/create_one_api_comments_post)
Create One
GET
[/api/comments/{item_id}](https://demo.mealie.io/docs#/Recipe:%20Comments/get_one_api_comments__item_id__get)
Get One
PUT
[/api/comments/{item_id}](https://demo.mealie.io/docs#/Recipe:%20Comments/update_one_api_comments__item_id__put)
Update One
DELETE
[/api/comments/{item_id}](https://demo.mealie.io/docs#/Recipe:%20Comments/delete_one_api_comments__item_id__delete)
Delete One
### [Recipe: Bulk Actions](https://demo.mealie.io/docs#/Recipe:%20Bulk%20Actions)
POST
[/api/recipes/bulk-actions/tag](https://demo.mealie.io/docs#/Recipe:%20Bulk%20Actions/bulk_tag_recipes_api_recipes_bulk_actions_tag_post)
Bulk Tag Recipes
POST
[/api/recipes/bulk-actions/settings](https://demo.mealie.io/docs#/Recipe:%20Bulk%20Actions/bulk_settings_recipes_api_recipes_bulk_actions_settings_post)
Bulk Settings Recipes
POST
[/api/recipes/bulk-actions/categorize](https://demo.mealie.io/docs#/Recipe:%20Bulk%20Actions/bulk_categorize_recipes_api_recipes_bulk_actions_categorize_post)
Bulk Categorize Recipes
POST
[/api/recipes/bulk-actions/delete](https://demo.mealie.io/docs#/Recipe:%20Bulk%20Actions/bulk_delete_recipes_api_recipes_bulk_actions_delete_post)
Bulk Delete Recipes
POST
[/api/recipes/bulk-actions/export](https://demo.mealie.io/docs#/Recipe:%20Bulk%20Actions/bulk_export_recipes_api_recipes_bulk_actions_export_post)
Bulk Export Recipes
GET
[/api/recipes/bulk-actions/export](https://demo.mealie.io/docs#/Recipe:%20Bulk%20Actions/get_exported_data_api_recipes_bulk_actions_export_get)
Get Exported Data
GET
[/api/recipes/bulk-actions/export/{export_id}/download](https://demo.mealie.io/docs#/Recipe:%20Bulk%20Actions/get_exported_data_token_api_recipes_bulk_actions_export__export_id__download_get)
Get Exported Data Token
DELETE
[/api/recipes/bulk-actions/export/purge](https://demo.mealie.io/docs#/Recipe:%20Bulk%20Actions/purge_export_data_api_recipes_bulk_actions_export_purge_delete)
Purge Export Data
### [Recipe: Shared](https://demo.mealie.io/docs#/Recipe:%20Shared)
GET
[/api/recipes/shared/{token_id}](https://demo.mealie.io/docs#/Recipe:%20Shared/get_shared_recipe_api_recipes_shared__token_id__get)
Get Shared Recipe
GET
[/api/recipes/shared/{token_id}/zip](https://demo.mealie.io/docs#/Recipe:%20Shared/get_shared_recipe_as_zip_api_recipes_shared__token_id__zip_get)
Get Shared Recipe As Zip
### [Recipe: Timeline](https://demo.mealie.io/docs#/Recipe:%20Timeline)
GET
[/api/recipes/timeline/events](https://demo.mealie.io/docs#/Recipe:%20Timeline/get_all_api_recipes_timeline_events_get)
Get All
POST
[/api/recipes/timeline/events](https://demo.mealie.io/docs#/Recipe:%20Timeline/create_one_api_recipes_timeline_events_post)
Create One
GET
[/api/recipes/timeline/events/{item_id}](https://demo.mealie.io/docs#/Recipe:%20Timeline/get_one_api_recipes_timeline_events__item_id__get)
Get One
PUT
[/api/recipes/timeline/events/{item_id}](https://demo.mealie.io/docs#/Recipe:%20Timeline/update_one_api_recipes_timeline_events__item_id__put)
Update One
DELETE
[/api/recipes/timeline/events/{item_id}](https://demo.mealie.io/docs#/Recipe:%20Timeline/delete_one_api_recipes_timeline_events__item_id__delete)
Delete One
PUT
[/api/recipes/timeline/events/{item_id}/image](https://demo.mealie.io/docs#/Recipe:%20Timeline/update_event_image_api_recipes_timeline_events__item_id__image_put)
Update Event Image
### [Organizer: Categories](https://demo.mealie.io/docs#/Organizer:%20Categories)
GET
[/api/organizers/categories](https://demo.mealie.io/docs#/Organizer:%20Categories/get_all_api_organizers_categories_get)
Get All
POST
[/api/organizers/categories](https://demo.mealie.io/docs#/Organizer:%20Categories/create_one_api_organizers_categories_post)
Create One
GET
[/api/organizers/categories/empty](https://demo.mealie.io/docs#/Organizer:%20Categories/get_all_empty_api_organizers_categories_empty_get)
Get All Empty
GET
[/api/organizers/categories/{item_id}](https://demo.mealie.io/docs#/Organizer:%20Categories/get_one_api_organizers_categories__item_id__get)
Get One
PUT
[/api/organizers/categories/{item_id}](https://demo.mealie.io/docs#/Organizer:%20Categories/update_one_api_organizers_categories__item_id__put)
Update One
DELETE
[/api/organizers/categories/{item_id}](https://demo.mealie.io/docs#/Organizer:%20Categories/delete_one_api_organizers_categories__item_id__delete)
Delete One
GET
[/api/organizers/categories/slug/{category_slug}](https://demo.mealie.io/docs#/Organizer:%20Categories/get_one_by_slug_api_organizers_categories_slug__category_slug__get)
Get One By Slug
### [Organizer: Tags](https://demo.mealie.io/docs#/Organizer:%20Tags)
GET
[/api/organizers/tags](https://demo.mealie.io/docs#/Organizer:%20Tags/get_all_api_organizers_tags_get)
Get All
POST
[/api/organizers/tags](https://demo.mealie.io/docs#/Organizer:%20Tags/create_one_api_organizers_tags_post)
Create One
GET
[/api/organizers/tags/empty](https://demo.mealie.io/docs#/Organizer:%20Tags/get_empty_tags_api_organizers_tags_empty_get)
Get Empty Tags
GET
[/api/organizers/tags/{item_id}](https://demo.mealie.io/docs#/Organizer:%20Tags/get_one_api_organizers_tags__item_id__get)
Get One
PUT
[/api/organizers/tags/{item_id}](https://demo.mealie.io/docs#/Organizer:%20Tags/update_one_api_organizers_tags__item_id__put)
Update One
DELETE
[/api/organizers/tags/{item_id}](https://demo.mealie.io/docs#/Organizer:%20Tags/delete_recipe_tag_api_organizers_tags__item_id__delete)
Delete Recipe Tag
GET
[/api/organizers/tags/slug/{tag_slug}](https://demo.mealie.io/docs#/Organizer:%20Tags/get_one_by_slug_api_organizers_tags_slug__tag_slug__get)
Get One By Slug
### [Organizer: Tools](https://demo.mealie.io/docs#/Organizer:%20Tools)
GET
[/api/organizers/tools](https://demo.mealie.io/docs#/Organizer:%20Tools/get_all_api_organizers_tools_get)
Get All
POST
[/api/organizers/tools](https://demo.mealie.io/docs#/Organizer:%20Tools/create_one_api_organizers_tools_post)
Create One
GET
[/api/organizers/tools/{item_id}](https://demo.mealie.io/docs#/Organizer:%20Tools/get_one_api_organizers_tools__item_id__get)
Get One
PUT
[/api/organizers/tools/{item_id}](https://demo.mealie.io/docs#/Organizer:%20Tools/update_one_api_organizers_tools__item_id__put)
Update One
DELETE
[/api/organizers/tools/{item_id}](https://demo.mealie.io/docs#/Organizer:%20Tools/delete_one_api_organizers_tools__item_id__delete)
Delete One
GET
[/api/organizers/tools/slug/{tool_slug}](https://demo.mealie.io/docs#/Organizer:%20Tools/get_one_by_slug_api_organizers_tools_slug__tool_slug__get)
Get One By Slug
### [Shared: Recipes](https://demo.mealie.io/docs#/Shared:%20Recipes)
GET
[/api/shared/recipes](https://demo.mealie.io/docs#/Shared:%20Recipes/get_all_api_shared_recipes_get)
Get All
POST
[/api/shared/recipes](https://demo.mealie.io/docs#/Shared:%20Recipes/create_one_api_shared_recipes_post)
Create One
GET
[/api/shared/recipes/{item_id}](https://demo.mealie.io/docs#/Shared:%20Recipes/get_one_api_shared_recipes__item_id__get)
Get One
DELETE
[/api/shared/recipes/{item_id}](https://demo.mealie.io/docs#/Shared:%20Recipes/delete_one_api_shared_recipes__item_id__delete)
Delete One
### [Recipe: Ingredient Parser](https://demo.mealie.io/docs#/Recipe:%20Ingredient%20Parser)
POST
[/api/parser/ingredient](https://demo.mealie.io/docs#/Recipe:%20Ingredient%20Parser/parse_ingredient_api_parser_ingredient_post)
Parse Ingredient
POST
[/api/parser/ingredients](https://demo.mealie.io/docs#/Recipe:%20Ingredient%20Parser/parse_ingredients_api_parser_ingredients_post)
Parse Ingredients
### [Recipes: Foods](https://demo.mealie.io/docs#/Recipes:%20Foods)
GET
[/api/foods](https://demo.mealie.io/docs#/Recipes:%20Foods/get_all_api_foods_get)
Get All
POST
[/api/foods](https://demo.mealie.io/docs#/Recipes:%20Foods/create_one_api_foods_post)
Create One
PUT
[/api/foods/merge](https://demo.mealie.io/docs#/Recipes:%20Foods/merge_one_api_foods_merge_put)
Merge One
GET
[/api/foods/{item_id}](https://demo.mealie.io/docs#/Recipes:%20Foods/get_one_api_foods__item_id__get)
Get One
PUT
[/api/foods/{item_id}](https://demo.mealie.io/docs#/Recipes:%20Foods/update_one_api_foods__item_id__put)
Update One
DELETE
[/api/foods/{item_id}](https://demo.mealie.io/docs#/Recipes:%20Foods/delete_one_api_foods__item_id__delete)
Delete One
### [Recipes: Units](https://demo.mealie.io/docs#/Recipes:%20Units)
GET
[/api/units](https://demo.mealie.io/docs#/Recipes:%20Units/get_all_api_units_get)
Get All
POST
[/api/units](https://demo.mealie.io/docs#/Recipes:%20Units/create_one_api_units_post)
Create One
PUT
[/api/units/merge](https://demo.mealie.io/docs#/Recipes:%20Units/merge_one_api_units_merge_put)
Merge One
GET
[/api/units/{item_id}](https://demo.mealie.io/docs#/Recipes:%20Units/get_one_api_units__item_id__get)
Get One
PUT
[/api/units/{item_id}](https://demo.mealie.io/docs#/Recipes:%20Units/update_one_api_units__item_id__put)
Update One
DELETE
[/api/units/{item_id}](https://demo.mealie.io/docs#/Recipes:%20Units/delete_one_api_units__item_id__delete)
Delete One
### [Admin: About](https://demo.mealie.io/docs#/Admin:%20About)
GET
[/api/admin/about](https://demo.mealie.io/docs#/Admin:%20About/get_app_info_api_admin_about_get)
Get App Info
GET
[/api/admin/about/statistics](https://demo.mealie.io/docs#/Admin:%20About/get_app_statistics_api_admin_about_statistics_get)
Get App Statistics
GET
[/api/admin/about/check](https://demo.mealie.io/docs#/Admin:%20About/check_app_config_api_admin_about_check_get)
Check App Config
### [Admin: Manage Users](https://demo.mealie.io/docs#/Admin:%20Manage%20Users)
GET
[/api/admin/users](https://demo.mealie.io/docs#/Admin:%20Manage%20Users/get_all_api_admin_users_get)
Get All
POST
[/api/admin/users](https://demo.mealie.io/docs#/Admin:%20Manage%20Users/create_one_api_admin_users_post)
Create One
POST
[/api/admin/users/unlock](https://demo.mealie.io/docs#/Admin:%20Manage%20Users/unlock_users_api_admin_users_unlock_post)
Unlock Users
GET
[/api/admin/users/{item_id}](https://demo.mealie.io/docs#/Admin:%20Manage%20Users/get_one_api_admin_users__item_id__get)
Get One
PUT
[/api/admin/users/{item_id}](https://demo.mealie.io/docs#/Admin:%20Manage%20Users/update_one_api_admin_users__item_id__put)
Update One
DELETE
[/api/admin/users/{item_id}](https://demo.mealie.io/docs#/Admin:%20Manage%20Users/delete_one_api_admin_users__item_id__delete)
Delete One
POST
[/api/admin/users/password-reset-token](https://demo.mealie.io/docs#/Admin:%20Manage%20Users/generate_token_api_admin_users_password_reset_token_post)
Generate Token
### [Admin: Manage Households](https://demo.mealie.io/docs#/Admin:%20Manage%20Households)
GET
[/api/admin/households](https://demo.mealie.io/docs#/Admin:%20Manage%20Households/get_all_api_admin_households_get)
Get All
POST
[/api/admin/households](https://demo.mealie.io/docs#/Admin:%20Manage%20Households/create_one_api_admin_households_post)
Create One
GET
[/api/admin/households/{item_id}](https://demo.mealie.io/docs#/Admin:%20Manage%20Households/get_one_api_admin_households__item_id__get)
Get One
PUT
[/api/admin/households/{item_id}](https://demo.mealie.io/docs#/Admin:%20Manage%20Households/update_one_api_admin_households__item_id__put)
Update One
DELETE
[/api/admin/households/{item_id}](https://demo.mealie.io/docs#/Admin:%20Manage%20Households/delete_one_api_admin_households__item_id__delete)
Delete One
### [Admin: Manage Groups](https://demo.mealie.io/docs#/Admin:%20Manage%20Groups)
GET
[/api/admin/groups](https://demo.mealie.io/docs#/Admin:%20Manage%20Groups/get_all_api_admin_groups_get)
Get All
POST
[/api/admin/groups](https://demo.mealie.io/docs#/Admin:%20Manage%20Groups/create_one_api_admin_groups_post)
Create One
GET
[/api/admin/groups/{item_id}](https://demo.mealie.io/docs#/Admin:%20Manage%20Groups/get_one_api_admin_groups__item_id__get)
Get One
PUT
[/api/admin/groups/{item_id}](https://demo.mealie.io/docs#/Admin:%20Manage%20Groups/update_one_api_admin_groups__item_id__put)
Update One
DELETE
[/api/admin/groups/{item_id}](https://demo.mealie.io/docs#/Admin:%20Manage%20Groups/delete_one_api_admin_groups__item_id__delete)
Delete One
### [Admin: Email](https://demo.mealie.io/docs#/Admin:%20Email)
GET
[/api/admin/email](https://demo.mealie.io/docs#/Admin:%20Email/check_email_config_api_admin_email_get)
Check Email Config
POST
[/api/admin/email](https://demo.mealie.io/docs#/Admin:%20Email/send_test_email_api_admin_email_post)
Send Test Email
### [Admin: Backups](https://demo.mealie.io/docs#/Admin:%20Backups)
GET
[/api/admin/backups](https://demo.mealie.io/docs#/Admin:%20Backups/get_all_api_admin_backups_get)
Get All
POST
[/api/admin/backups](https://demo.mealie.io/docs#/Admin:%20Backups/create_one_api_admin_backups_post)
Create One
GET
[/api/admin/backups/{file_name}](https://demo.mealie.io/docs#/Admin:%20Backups/get_one_api_admin_backups__file_name__get)
Get One
DELETE
[/api/admin/backups/{file_name}](https://demo.mealie.io/docs#/Admin:%20Backups/delete_one_api_admin_backups__file_name__delete)
Delete One
POST
[/api/admin/backups/upload](https://demo.mealie.io/docs#/Admin:%20Backups/upload_one_api_admin_backups_upload_post)
Upload One
POST
[/api/admin/backups/{file_name}/restore](https://demo.mealie.io/docs#/Admin:%20Backups/import_one_api_admin_backups__file_name__restore_post)
Import One
### [Admin: Maintenance](https://demo.mealie.io/docs#/Admin:%20Maintenance)
GET
[/api/admin/maintenance](https://demo.mealie.io/docs#/Admin:%20Maintenance/get_maintenance_summary_api_admin_maintenance_get)
Get Maintenance Summary
GET
[/api/admin/maintenance/storage](https://demo.mealie.io/docs#/Admin:%20Maintenance/get_storage_details_api_admin_maintenance_storage_get)
Get Storage Details
POST
[/api/admin/maintenance/clean/images](https://demo.mealie.io/docs#/Admin:%20Maintenance/clean_images_api_admin_maintenance_clean_images_post)
Clean Images
POST
[/api/admin/maintenance/clean/temp](https://demo.mealie.io/docs#/Admin:%20Maintenance/clean_temp_api_admin_maintenance_clean_temp_post)
Clean Temp
POST
[/api/admin/maintenance/clean/recipe-folders](https://demo.mealie.io/docs#/Admin:%20Maintenance/clean_recipe_folders_api_admin_maintenance_clean_recipe_folders_post)
Clean Recipe Folders
### [Admin: Debug](https://demo.mealie.io/docs#/Admin:%20Debug)
POST
[/api/admin/debug/openai](https://demo.mealie.io/docs#/Admin:%20Debug/debug_openai_api_admin_debug_openai_post)
Debug Openai
### [Explore: Foods](https://demo.mealie.io/docs#/Explore:%20Foods)
GET
[/api/explore/groups/{group_slug}/foods](https://demo.mealie.io/docs#/Explore:%20Foods/get_all_api_explore_groups__group_slug__foods_get)
Get All
GET
[/api/explore/groups/{group_slug}/foods/{item_id}](https://demo.mealie.io/docs#/Explore:%20Foods/get_one_api_explore_groups__group_slug__foods__item_id__get)
Get One
### [Explore: Households](https://demo.mealie.io/docs#/Explore:%20Households)
GET
[/api/explore/groups/{group_slug}/households](https://demo.mealie.io/docs#/Explore:%20Households/get_all_api_explore_groups__group_slug__households_get)
Get All
GET
[/api/explore/groups/{group_slug}/households/{household_slug}](https://demo.mealie.io/docs#/Explore:%20Households/get_household_api_explore_groups__group_slug__households__household_slug__get)
Get Household
### [Explore: Categories](https://demo.mealie.io/docs#/Explore:%20Categories)
GET
[/api/explore/groups/{group_slug}/organizers/categories](https://demo.mealie.io/docs#/Explore:%20Categories/get_all_api_explore_groups__group_slug__organizers_categories_get)
Get All
GET
[/api/explore/groups/{group_slug}/organizers/categories/{item_id}](https://demo.mealie.io/docs#/Explore:%20Categories/get_one_api_explore_groups__group_slug__organizers_categories__item_id__get)
Get One
### [Explore: Tags](https://demo.mealie.io/docs#/Explore:%20Tags)
GET
[/api/explore/groups/{group_slug}/organizers/tags](https://demo.mealie.io/docs#/Explore:%20Tags/get_all_api_explore_groups__group_slug__organizers_tags_get)
Get All
GET
[/api/explore/groups/{group_slug}/organizers/tags/{item_id}](https://demo.mealie.io/docs#/Explore:%20Tags/get_one_api_explore_groups__group_slug__organizers_tags__item_id__get)
Get One
### [Explore: Tools](https://demo.mealie.io/docs#/Explore:%20Tools)
GET
[/api/explore/groups/{group_slug}/organizers/tools](https://demo.mealie.io/docs#/Explore:%20Tools/get_all_api_explore_groups__group_slug__organizers_tools_get)
Get All
GET
[/api/explore/groups/{group_slug}/organizers/tools/{item_id}](https://demo.mealie.io/docs#/Explore:%20Tools/get_one_api_explore_groups__group_slug__organizers_tools__item_id__get)
Get One
### [Explore: Cookbooks](https://demo.mealie.io/docs#/Explore:%20Cookbooks)
GET
[/api/explore/groups/{group_slug}/cookbooks](https://demo.mealie.io/docs#/Explore:%20Cookbooks/get_all_api_explore_groups__group_slug__cookbooks_get)
Get All
GET
[/api/explore/groups/{group_slug}/cookbooks/{item_id}](https://demo.mealie.io/docs#/Explore:%20Cookbooks/get_one_api_explore_groups__group_slug__cookbooks__item_id__get)
Get One
### [Explore: Recipes](https://demo.mealie.io/docs#/Explore:%20Recipes)
GET
[/api/explore/groups/{group_slug}/recipes](https://demo.mealie.io/docs#/Explore:%20Recipes/get_all_api_explore_groups__group_slug__recipes_get)
Get All
GET
[/api/explore/groups/{group_slug}/recipes/suggestions](https://demo.mealie.io/docs#/Explore:%20Recipes/suggest_recipes_api_explore_groups__group_slug__recipes_suggestions_get)
Suggest Recipes
GET
[/api/explore/groups/{group_slug}/recipes/{recipe_slug}](https://demo.mealie.io/docs#/Explore:%20Recipes/get_recipe_api_explore_groups__group_slug__recipes__recipe_slug__get)
Get Recipe
### [Utils](https://demo.mealie.io/docs#/Utils)
GET
[/api/utils/download](https://demo.mealie.io/docs#/Utils/download_file_api_utils_download_get)
Download File
#### Schemas
AdminAboutInfo
Expand all**object**
AllBackups
Expand all**object**
AppInfo
Expand all**object**
AppStartupInfo
Expand all**object**
AppStatistics
Expand all**object**
AppTheme
Expand all**object**
AssignCategories
Expand all**object**
AssignSettings
Expand all**object**
AssignTags
Expand all**object**
AuthMethod
Expand all**string**
BackupFile
Expand all**object**
Body_create_recipe_from_image_api_recipes_create_image_post
Expand all**object**
Body_create_recipe_from_zip_api_recipes_create_zip_post
Expand all**object**
Body_debug_openai_api_admin_debug_openai_post
Expand all**object**
Body_get_token_api_auth_token_post
Expand all**object**
Body_start_data_migration_api_groups_migrations_post
Expand all**object**
Body_trigger_action_api_households_recipe_actions__item_id__trigger__recipe_slug__post
Expand all**object**
Body_update_event_image_api_recipes_timeline_events__item_id__image_put
Expand all**object**
Body_update_recipe_image_api_recipes__slug__image_put
Expand all**object**
Body_update_user_image_api_users__id__image_post
Expand all**object**
Body_upload_one_api_admin_backups_upload_post
Expand all**object**
Body_upload_recipe_asset_api_recipes__slug__assets_post
Expand all**object**
CategoryBase
Expand all**object**
CategoryIn
Expand all**object**
CategoryOut
Expand all**object**
CategorySummary
Expand all**object**
ChangePassword
Expand all**object**
CheckAppConfig
Expand all**object**
CookBookPagination
Expand all**object**
CookbookHousehold
Expand all**object**
CreateCookBook
Expand all**object**
CreateGroupRecipeAction
Expand all**object**
CreateIngredientFood
Expand all**object**
CreateIngredientFoodAlias
Expand all**object**
CreateIngredientUnit
Expand all**object**
CreateIngredientUnitAlias
Expand all**object**
CreateInviteToken
Expand all**object**
CreatePlanEntry
Expand all**object**
CreateRandomEntry
Expand all**object**
CreateRecipe
Expand all**object**
CreateRecipeBulk
Expand all**object**
CreateRecipeByUrlBulk
Expand all**object**
CreateUserRegistration
Expand all**object**
CreateWebhook
Expand all**object**
DebugResponse
Expand all**object**
DeleteRecipes
Expand all**object**
DeleteTokenResponse
Expand all**object**
EmailInitationResponse
Expand all**object**
EmailInvitation
Expand all**object**
EmailReady
Expand all**object**
EmailSuccess
Expand all**object**
EmailTest
Expand all**object**
ExportRecipes
Expand all**object**
ExportTypes
Expand all**string**
FileTokenResponse
Expand all**object**
ForgotPassword
Expand all**object**
FormatResponse
Expand all**object**
GroupAdminUpdate
Expand all**object**
GroupBase
Expand all**object**
GroupDataExport
Expand all**object**
GroupEventNotifierCreate
Expand all**object**
GroupEventNotifierOptions
Expand all**object**
GroupEventNotifierOptionsOut
Expand all**object**
GroupEventNotifierOut
Expand all**object**
GroupEventNotifierUpdate
Expand all**object**
GroupEventPagination
Expand all**object**
GroupHouseholdSummary
Expand all**object**
GroupInDB
Expand all**object**
GroupPagination
Expand all**object**
GroupRecipeActionOut
Expand all**object**
GroupRecipeActionPagination
Expand all**object**
GroupRecipeActionType
Expand all**string**
GroupStorage
Expand all**object**
GroupSummary
Expand all**object**
HTTPValidationError
Expand all**object**
HouseholdCreate
Expand all**object**
HouseholdInDB
Expand all**object**
HouseholdPagination
Expand all**object**
HouseholdRecipeSummary
Expand all**object**
HouseholdStatistics
Expand all**object**
HouseholdSummary
Expand all**object**
HouseholdUserSummary
Expand all**object**
ImageType
Expand all**string**
IngredientConfidence
Expand all**object**
IngredientFood
Expand all**object**
IngredientFood
Expand all**object**
IngredientFoodAlias
Expand all**object**
IngredientFoodPagination
Expand all**object**
IngredientReferences
Expand all**object**
IngredientRequest
Expand all**object**
IngredientUnit
Expand all**object**
IngredientUnit
Expand all**object**
IngredientUnitAlias
Expand all**object**
IngredientUnitPagination
Expand all**object**
IngredientsRequest
Expand all**object**
LogicalOperator
Expand all**string**
LongLiveTokenCreateResponse
Expand all**object**
LongLiveTokenIn
Expand all**object**
LongLiveTokenOut
Expand all**object**
MaintenanceStorageDetails
Expand all**object**
MaintenanceSummary
Expand all**object**
MergeFood
Expand all**object**
MergeUnit
Expand all**object**
MultiPurposeLabelCreate
Expand all**object**
MultiPurposeLabelOut
Expand all**object**
MultiPurposeLabelPagination
Expand all**object**
MultiPurposeLabelSummary
Expand all**object**
MultiPurposeLabelUpdate
Expand all**object**
Nutrition
Expand all**object**
OrderByNullPosition
Expand all**string**
OrderDirection
Expand all**string**
PaginationBase[HouseholdSummary]
Expand all**object**
PaginationBase[IngredientFood]
Expand all**object**
PaginationBase[ReadCookBook]
Expand all**object**
PaginationBase[RecipeCategory]
Expand all**object**
PaginationBase[RecipeSummary]
Expand all**object**
PaginationBase[RecipeTag]
Expand all**object**
PaginationBase[RecipeTool]
Expand all**object**
PaginationBase[UserOut]
Expand all**object**
PaginationBase[UserSummary]
Expand all**object**
ParsedIngredient
Expand all**object**
PasswordResetToken
Expand all**object**
PlanEntryPagination
Expand all**object**
PlanEntryType
Expand all**string**
PlanRulesCreate
Expand all**object**
PlanRulesDay
Expand all**string**
PlanRulesOut
Expand all**object**
PlanRulesPagination
Expand all**object**
PlanRulesType
Expand all**string**
QueryFilterJSON
Expand all**object**
QueryFilterJSONPart
Expand all**object**
ReadCookBook
Expand all**object**
ReadGroupPreferences
Expand all**object**
ReadHouseholdPreferences
Expand all**object**
ReadInviteToken
Expand all**object**
ReadPlanEntry
Expand all**object**
ReadWebhook
Expand all**object**
Recipe
Expand all**object**
Recipe
Expand all**object**
RecipeAsset
Expand all**object**
RecipeCategory
Expand all**object**
RecipeCategoryPagination
Expand all**object**
RecipeCommentCreate
Expand all**object**
RecipeCommentOut
Expand all**object**
RecipeCommentOut
Expand all**object**
RecipeCommentPagination
Expand all**object**
RecipeCommentUpdate
Expand all**object**
RecipeDuplicate
Expand all**object**
RecipeIngredient
Expand all**object**
RecipeIngredient
Expand all**object**
RecipeLastMade
Expand all**object**
RecipeNote
Expand all**object**
RecipeSettings
Expand all**object**
RecipeShareToken
Expand all**object**
RecipeShareTokenCreate
Expand all**object**
RecipeShareTokenSummary
Expand all**object**
RecipeStep
Expand all**object**
RecipeSuggestionResponse
Expand all**object**
RecipeSuggestionResponseItem
Expand all**object**
RecipeSummary
Expand all**object**
RecipeTag
Expand all**object**
RecipeTagPagination
Expand all**object**
RecipeTagResponse
Expand all**object**
RecipeTimelineEventIn
Expand all**object**
RecipeTimelineEventOut
Expand all**object**
RecipeTimelineEventPagination
Expand all**object**
RecipeTimelineEventUpdate
Expand all**object**
RecipeTool
Expand all**object**
RecipeToolCreate
Expand all**object**
RecipeToolOut
Expand all**object**
RecipeToolPagination
Expand all**object**
RecipeToolResponse
Expand all**object**
RegisteredParser
Expand all**string**
RelationalKeyword
Expand all**string**
RelationalOperator
Expand all**string**
ReportCategory
Expand all**string**
ReportEntryOut
Expand all**object**
ReportOut
Expand all**object**
ReportSummary
Expand all**object**
ReportSummaryStatus
Expand all**string**
ResetPassword
Expand all**object**
SaveGroupRecipeAction
Expand all**object**
ScrapeRecipe
Expand all**object**
ScrapeRecipeData
Expand all**object**
ScrapeRecipeTest
Expand all**object**
SeederConfig
Expand all**object**
SetPermissions
Expand all**object**
ShoppingListAddRecipeParams
Expand all**object**
ShoppingListAddRecipeParamsBulk
Expand all**object**
ShoppingListCreate
Expand all**object**
ShoppingListItemCreate
Expand all**object**
ShoppingListItemOut
Expand all**object**
ShoppingListItemOut
Expand all**object**
ShoppingListItemPagination
Expand all**object**
ShoppingListItemRecipeRefCreate
Expand all**object**
ShoppingListItemRecipeRefOut
Expand all**object**
ShoppingListItemRecipeRefUpdate
Expand all**object**
ShoppingListItemUpdate
Expand all**object**
ShoppingListItemUpdateBulk
Expand all**object**
ShoppingListItemsCollectionOut
Expand all**object**
ShoppingListMultiPurposeLabelOut
Expand all**object**
ShoppingListMultiPurposeLabelUpdate
Expand all**object**
ShoppingListOut
Expand all**object**
ShoppingListPagination
Expand all**object**
ShoppingListRecipeRefOut
Expand all**object**
ShoppingListRemoveRecipeParams
Expand all**object**
ShoppingListSummary
Expand all**object**
ShoppingListUpdate
Expand all**object**
SuccessResponse
Expand all**object**
SupportedMigrations
Expand all**string**
TagBase
Expand all**object**
TagIn
Expand all**object**
TagOut
Expand all**object**
TimelineEventImage
Expand all**string**
TimelineEventType
Expand all**string**
UnlockResults
Expand all**object**
UpdateCookBook
Expand all**object**
UpdateGroupPreferences
Expand all**object**
UpdateHouseholdAdmin
Expand all**object**
UpdateHouseholdPreferences
Expand all**object**
UpdateImageResponse
Expand all**object**
UpdatePlanEntry
Expand all**object**
UserBase
Expand all**object**
UserIn
Expand all**object**
UserOut
Expand all**object**
UserPagination
Expand all**object**
UserRatingOut
Expand all**object**
UserRatingSummary
Expand all**object**
UserRatingUpdate
Expand all**object**
UserRatings[UserRatingOut]
Expand all**object**
UserRatings[UserRatingSummary]
Expand all**object**
UserSummary
Expand all**object**
ValidationError
Expand all**object**
WebhookPagination
Expand all**object**
WebhookType
Expand all**string**
UserBase
Expand all**object**
UserBase
Expand all**object**
