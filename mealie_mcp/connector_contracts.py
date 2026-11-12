"""Surface contracts: tool use, links, data locations and business roles."""

from scion_sdk.surface_contracts import (
    BusinessRole,
    DataLocation,
    Refusal,
    SurfaceLink,
    ToolStep,
    ToolUseContract,
)

CONTRACTS = (
    ToolUseContract(
        "mealie-manage-rating",
        (
            ToolStep(
                "mealie_get_favorites",
                params=(
                    "accept_language",
                    "id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_logged_in_user_favorites",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_logged_in_user_rating_for_recipe",
                params=(
                    "accept_language",
                    "recipe_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_logged_in_user_ratings",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_ratings",
                params=(
                    "accept_language",
                    "id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_add_favorite",
                params=(
                    "accept_language",
                    "id",
                    "slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_set_rating",
                params=(
                    "accept_language",
                    "data",
                    "id",
                    "slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_remove_favorite",
                params=(
                    "accept_language",
                    "confirm",
                    "id",
                    "slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-profile",
        (
            ToolStep(
                "mealie_get_logged_in_user",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_user_image",
                params=(
                    "file_name",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_create",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_register_new_user",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_update_user",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_update_user_image",
                params=(
                    "accept_language",
                    "data",
                    "id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete",
                params=(
                    "accept_language",
                    "confirm",
                    "token_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-admin-user",
        (
            ToolStep(
                "mealie_get_admin_users",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_admin_users_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_post_admin_users",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_admin_users_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_admin_users_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-auth",
        (
            ToolStep(
                "mealie_get_token",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_forgot_password",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_generate_token",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_logout",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_oauth_callback",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_oauth_login",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_refresh_token",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_update_password",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_reset_password",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-inspect-explore-catalog",
        (
            ToolStep(
                "mealie_get_explore_groups_group_slug_cookbooks",
                params=(
                    "accept_language",
                    "group_slug",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                    "search",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_explore_groups_group_slug_cookbooks_item_id",
                params=(
                    "accept_language",
                    "group_slug",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_explore_groups_group_slug_foods",
                params=(
                    "accept_language",
                    "group_slug",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                    "search",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_explore_groups_group_slug_foods_item_id",
                params=(
                    "accept_language",
                    "group_slug",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_explore_groups_group_slug_households",
                params=(
                    "accept_language",
                    "group_slug",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-inspect-explore-organizer",
        (
            ToolStep(
                "mealie_get_explore_groups_group_slug_organizers_categories",
                params=(
                    "accept_language",
                    "group_slug",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                    "search",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_explore_groups_group_slug_organizers_categories_item_id",
                params=(
                    "accept_language",
                    "group_slug",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_explore_groups_group_slug_organizers_tags",
                params=(
                    "accept_language",
                    "group_slug",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                    "search",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_explore_groups_group_slug_organizers_tags_item_id",
                params=(
                    "accept_language",
                    "group_slug",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_explore_groups_group_slug_organizers_tools",
                params=(
                    "accept_language",
                    "group_slug",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                    "search",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_explore_groups_group_slug_organizers_tools_item_id",
                params=(
                    "accept_language",
                    "group_slug",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-inspect-explore-recipe",
        (
            ToolStep(
                "mealie_get_explore_groups_group_slug_recipes",
                params=(
                    "accept_language",
                    "categories",
                    "cookbook",
                    "foods",
                    "group_slug",
                    "households",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                    "require_all_categories",
                    "require_all_foods",
                    "require_all_tags",
                    "require_all_tools",
                    "search",
                    "tags",
                    "tools",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_explore_groups_group_slug_recipes_suggestions",
                params=(
                    "accept_language",
                    "foods",
                    "group_slug",
                    "include_foods_on_hand",
                    "include_tools_on_hand",
                    "limit",
                    "max_missing_foods",
                    "max_missing_tools",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "pagination_seed",
                    "query_filter",
                    "tools",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-app",
        (
            ToolStep(
                "mealie_check_app_config",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_check_email_config",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_app_info",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_app_statistics",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_app_theme",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_startup_info",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_validation_text",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_send_test_email",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_debug_openai",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-maintenance",
        (
            ToolStep(
                "mealie_get_maintenance_summary",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_storage",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_storage_details",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_clean_images",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "mealie_clean_recipe_folders",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "mealie_clean_temp",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-backup",
        (
            ToolStep(
                "mealie_get_admin_backups",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_admin_backups_file_name",
                params=(
                    "accept_language",
                    "file_name",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_exported_data",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_exported_data_token",
                params=(
                    "accept_language",
                    "export_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_post_admin_backups",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_download_file",
                params=("token",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_admin_backups_file_name",
                params=(
                    "accept_language",
                    "confirm",
                    "file_name",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "mealie_purge_export_data",
                params=(
                    "accept_language",
                    "confirm",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-group-admin",
        (
            ToolStep(
                "mealie_get_admin_groups",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_admin_groups_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_admin_households",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_admin_households_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_all_households",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_post_admin_groups",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_post_admin_households",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_admin_groups_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_admin_households_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_admin_groups_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_admin_households_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-category",
        (
            ToolStep(
                "mealie_get_organizers_categories",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                    "search",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_organizers_categories_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_organizers_categories_slug_category_slug",
                params=(
                    "accept_language",
                    "category_slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_post_organizers_categories",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_organizers_categories_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_organizers_categories_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-tool",
        (
            ToolStep(
                "mealie_get_organizers_tools",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                    "search",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_organizers_tools_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_organizers_tools_slug_tool_slug",
                params=(
                    "accept_language",
                    "tool_slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_post_organizers_tools",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_organizers_tools_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_organizers_tools_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-tag",
        (
            ToolStep(
                "mealie_get_empty_tags",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_organizers_tags",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                    "search",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_organizers_tags_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_organizers_tags_slug_tag_slug",
                params=(
                    "accept_language",
                    "tag_slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_post_organizers_tags",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_organizers_tags_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_recipe_tag",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-inspect-organizer",
        (
            ToolStep(
                "mealie_get_all_empty",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-shared-recipe",
        (
            ToolStep(
                "mealie_get_shared_recipe",
                params=("token_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_shared_recipe_as_zip",
                params=("token_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_shared_recipes",
                params=(
                    "accept_language",
                    "recipe_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_shared_recipes_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_post_shared_recipes",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_shared_recipes_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-shopping",
        (
            ToolStep(
                "mealie_get_households_shopping_items",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_households_shopping_items_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_households_shopping_lists",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_households_shopping_lists_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_add_recipe_ingredients_to_list",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_add_single_recipe_ingredients_to_list",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                    "recipe_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_post_households_shopping_items",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_post_households_shopping_items_create_bulk",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_post_households_shopping_lists",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_households_shopping_items",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_households_shopping_items_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_households_shopping_lists_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_households_shopping_items",
                params=(
                    "accept_language",
                    "confirm",
                    "ids",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_households_shopping_items_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_households_shopping_lists_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-household",
        (
            ToolStep(
                "mealie_get_group_member",
                params=(
                    "accept_language",
                    "username_or_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_group_members",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_group_preferences",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_household",
                params=(
                    "accept_language",
                    "group_slug",
                    "household_slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_household_members",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_household_preferences",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_household_recipe",
                params=(
                    "accept_language",
                    "recipe_slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_invite_tokens",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_logged_in_user_group",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_logged_in_user_household",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_one_household",
                params=(
                    "accept_language",
                    "household_slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_statistics",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_create_invite_token",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_email_invitation",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_set_member_permissions",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_update_group_preferences",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_update_household_preferences",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-mealplan",
        (
            ToolStep(
                "mealie_get_households_mealplans",
                params=(
                    "accept_language",
                    "end_date",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                    "start_date",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_households_mealplans_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_households_mealplans_rules",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_households_mealplans_rules_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_todays_meals",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_create_random_meal",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_post_households_mealplans",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_post_households_mealplans_rules",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_households_mealplans_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_households_mealplans_rules_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_households_mealplans_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_households_mealplans_rules_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-label",
        (
            ToolStep(
                "mealie_get_groups_labels",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                    "search",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_groups_labels_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_post_groups_labels",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_groups_labels_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_seed_labels",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_update_label_settings",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_groups_labels_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-report",
        (
            ToolStep(
                "mealie_get_groups_reports",
                params=(
                    "accept_language",
                    "report_type",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_groups_reports_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_delete_groups_reports_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-cookbook",
        (
            ToolStep(
                "mealie_get_households_cookbooks",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_households_cookbooks_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_post_households_cookbooks",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_households_cookbooks",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_households_cookbooks_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_households_cookbooks_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-automation",
        (
            ToolStep(
                "mealie_get_households_events_notifications",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_households_events_notifications_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_households_recipe_actions",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_households_recipe_actions_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_households_webhooks",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_households_webhooks_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_post_households_events_notifications",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_post_households_recipe_actions",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_post_households_webhooks",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_households_events_notifications_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_households_recipe_actions_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_households_webhooks_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_rerun_webhooks",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_test_notification",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_test_one",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_trigger_action",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                    "recipe_slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_households_events_notifications_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_households_recipe_actions_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_households_webhooks_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-food",
        (
            ToolStep(
                "mealie_get_foods",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                    "search",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_foods_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_post_foods",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_recipe_food_create",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_foods_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_recipe_foods",
                params=(
                    "page",
                    "per_page",
                    "search",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_seed_foods",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_foods_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_foods_merge",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-unit",
        (
            ToolStep(
                "mealie_get_units",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                    "search",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_units_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_post_units",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_recipe_unit_create",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_units_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_recipe_units",
                params=(
                    "page",
                    "per_page",
                    "search",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_seed_units",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_units_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_units_merge",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-inspect-parser",
        (
            ToolStep(
                "mealie_parse_ingredient",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_parse_ingredients",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_post_parser_ingredient",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-recipe-bulk",
        (
            ToolStep(
                "mealie_bulk_categorize_recipes",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_bulk_export_recipes",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_bulk_settings_recipes",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_bulk_tag_recipes",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_bulk_delete_recipes",
                params=(
                    "accept_language",
                    "confirm",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-recipe-import",
        (
            ToolStep(
                "mealie_parse_recipe_url",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_parse_recipe_url_bulk",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_test_parse_recipe_url",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_create_recipe_from_html_or_json",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_create_recipe_from_image",
                params=(
                    "accept_language",
                    "data",
                    "translate_language",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_create_recipe_from_zip",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_upload_one",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_import_one",
                params=(
                    "accept_language",
                    "file_name",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_ingest_recipes",
                params=(
                    "ingest_images",
                    "params_json",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_scrape_image_url",
                params=(
                    "accept_language",
                    "data",
                    "slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_start_data_migration",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-recipe-media",
        (
            ToolStep(
                "mealie_get_recipe_as_format",
                params=(
                    "accept_language",
                    "slug",
                    "template_name",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_recipe_asset",
                params=(
                    "file_name",
                    "recipe_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_recipe_formats_and_templates",
                params=("accept_language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_recipe_img",
                params=(
                    "file_name",
                    "recipe_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_recipe_timeline_event_img",
                params=(
                    "file_name",
                    "recipe_id",
                    "timeline_event_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_upload_recipe_asset",
                params=(
                    "accept_language",
                    "data",
                    "slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_update_event_image",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_update_recipe_image",
                params=(
                    "accept_language",
                    "data",
                    "slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_recipe_image",
                params=(
                    "accept_language",
                    "confirm",
                    "slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-recipe",
        (
            ToolStep(
                "mealie_get_recipe",
                params=(
                    "accept_language",
                    "group_slug",
                    "recipe_slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_recipes",
                params=(
                    "accept_language",
                    "categories",
                    "cookbook",
                    "foods",
                    "households",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                    "require_all_categories",
                    "require_all_foods",
                    "require_all_tags",
                    "require_all_tools",
                    "search",
                    "tags",
                    "tools",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_recipes_slug",
                params=(
                    "accept_language",
                    "slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_recipes_suggestions",
                params=(
                    "accept_language",
                    "foods",
                    "include_foods_on_hand",
                    "include_tools_on_hand",
                    "limit",
                    "max_missing_foods",
                    "max_missing_tools",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "pagination_seed",
                    "query_filter",
                    "tools",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_post_recipes",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_recipe_create",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_duplicate_one",
                params=(
                    "accept_language",
                    "data",
                    "slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_patch_many",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_patch_one",
                params=(
                    "accept_language",
                    "data",
                    "slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_recipes",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_recipes_slug",
                params=(
                    "accept_language",
                    "data",
                    "slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_recipe_patch",
                params=(
                    "data",
                    "slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_recipe_update",
                params=(
                    "data",
                    "slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_update_last_made",
                params=(
                    "accept_language",
                    "data",
                    "slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_recipes_slug",
                params=(
                    "accept_language",
                    "confirm",
                    "slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "mealie_remove_recipe_ingredients_from_list",
                params=(
                    "accept_language",
                    "confirm",
                    "data",
                    "item_id",
                    "recipe_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "mealie_unlock_users",
                params=(
                    "accept_language",
                    "force",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-recipe-timeline",
        (
            ToolStep(
                "mealie_get_recipes_timeline_events",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_recipes_timeline_events_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_post_recipes_timeline_events",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_recipes_timeline_events_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_delete_recipes_timeline_events_item_id",
                params=(
                    "accept_language",
                    "confirm",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "mealie-manage-recipe-comment",
        (
            ToolStep(
                "mealie_get_comments",
                params=(
                    "accept_language",
                    "order_by",
                    "order_by_null_position",
                    "order_direction",
                    "page",
                    "pagination_seed",
                    "per_page",
                    "query_filter",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_comments_item_id",
                params=(
                    "accept_language",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_get_recipe_comments",
                params=(
                    "accept_language",
                    "slug",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "mealie_post_comments",
                params=(
                    "accept_language",
                    "data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "mealie_put_comments_item_id",
                params=(
                    "accept_language",
                    "data",
                    "item_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
)

LINKS = (
    SurfaceLink(
        "mealie-manage-rating",
        tools=(
            "mealie_add_favorite",
            "mealie_get_favorites",
            "mealie_get_logged_in_user_favorites",
            "mealie_get_logged_in_user_rating_for_recipe",
            "mealie_get_logged_in_user_ratings",
            "mealie_get_ratings",
            "mealie_remove_favorite",
            "mealie_set_rating",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-household-administrator",
        ),
        skills=("mealie-accounts",),
    ),
    SurfaceLink(
        "mealie-manage-profile",
        tools=(
            "mealie_create",
            "mealie_delete",
            "mealie_get_logged_in_user",
            "mealie_get_user_image",
            "mealie_register_new_user",
            "mealie_update_user",
            "mealie_update_user_image",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-household-administrator",
        ),
        skills=("mealie-accounts",),
    ),
    SurfaceLink(
        "mealie-manage-admin-user",
        tools=(
            "mealie_delete_admin_users_item_id",
            "mealie_get_admin_users",
            "mealie_get_admin_users_item_id",
            "mealie_post_admin_users",
            "mealie_put_admin_users_item_id",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-household-administrator",
        ),
        skills=("mealie-accounts",),
    ),
    SurfaceLink(
        "mealie-manage-auth",
        tools=(
            "mealie_forgot_password",
            "mealie_generate_token",
            "mealie_get_token",
            "mealie_logout",
            "mealie_oauth_callback",
            "mealie_oauth_login",
            "mealie_refresh_token",
            "mealie_reset_password",
            "mealie_update_password",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-household-administrator",
        ),
        skills=("mealie-accounts",),
    ),
    SurfaceLink(
        "mealie-inspect-explore-catalog",
        tools=(
            "mealie_get_explore_groups_group_slug_cookbooks",
            "mealie_get_explore_groups_group_slug_cookbooks_item_id",
            "mealie_get_explore_groups_group_slug_foods",
            "mealie_get_explore_groups_group_slug_foods_item_id",
            "mealie_get_explore_groups_group_slug_households",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-browser",
        ),
        skills=("mealie-public-explore",),
    ),
    SurfaceLink(
        "mealie-inspect-explore-organizer",
        tools=(
            "mealie_get_explore_groups_group_slug_organizers_categories",
            "mealie_get_explore_groups_group_slug_organizers_categories_item_id",
            "mealie_get_explore_groups_group_slug_organizers_tags",
            "mealie_get_explore_groups_group_slug_organizers_tags_item_id",
            "mealie_get_explore_groups_group_slug_organizers_tools",
            "mealie_get_explore_groups_group_slug_organizers_tools_item_id",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-browser",
        ),
        skills=("mealie-public-explore",),
    ),
    SurfaceLink(
        "mealie-inspect-explore-recipe",
        tools=(
            "mealie_get_explore_groups_group_slug_recipes",
            "mealie_get_explore_groups_group_slug_recipes_suggestions",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-browser",
        ),
        skills=("mealie-public-explore",),
    ),
    SurfaceLink(
        "mealie-manage-app",
        tools=(
            "mealie_check_app_config",
            "mealie_check_email_config",
            "mealie_debug_openai",
            "mealie_get_app_info",
            "mealie_get_app_statistics",
            "mealie_get_app_theme",
            "mealie_get_startup_info",
            "mealie_get_validation_text",
            "mealie_send_test_email",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-household-administrator",
        ),
        skills=("mealie-server-administration",),
    ),
    SurfaceLink(
        "mealie-manage-maintenance",
        tools=(
            "mealie_clean_images",
            "mealie_clean_recipe_folders",
            "mealie_clean_temp",
            "mealie_get_maintenance_summary",
            "mealie_get_storage",
            "mealie_get_storage_details",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-household-administrator",
        ),
        skills=("mealie-server-administration",),
    ),
    SurfaceLink(
        "mealie-manage-backup",
        tools=(
            "mealie_delete_admin_backups_file_name",
            "mealie_download_file",
            "mealie_get_admin_backups",
            "mealie_get_admin_backups_file_name",
            "mealie_get_exported_data",
            "mealie_get_exported_data_token",
            "mealie_post_admin_backups",
            "mealie_purge_export_data",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-household-administrator",
        ),
        skills=("mealie-server-administration",),
    ),
    SurfaceLink(
        "mealie-manage-group-admin",
        tools=(
            "mealie_delete_admin_groups_item_id",
            "mealie_delete_admin_households_item_id",
            "mealie_get_admin_groups",
            "mealie_get_admin_groups_item_id",
            "mealie_get_admin_households",
            "mealie_get_admin_households_item_id",
            "mealie_get_all_households",
            "mealie_post_admin_groups",
            "mealie_post_admin_households",
            "mealie_put_admin_groups_item_id",
            "mealie_put_admin_households_item_id",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-household-administrator",
        ),
        skills=("mealie-server-administration",),
    ),
    SurfaceLink(
        "mealie-manage-category",
        tools=(
            "mealie_delete_organizers_categories_item_id",
            "mealie_get_organizers_categories",
            "mealie_get_organizers_categories_item_id",
            "mealie_get_organizers_categories_slug_category_slug",
            "mealie_post_organizers_categories",
            "mealie_put_organizers_categories_item_id",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-curator",
        ),
        skills=("mealie-organizer-operations",),
    ),
    SurfaceLink(
        "mealie-manage-tool",
        tools=(
            "mealie_delete_organizers_tools_item_id",
            "mealie_get_organizers_tools",
            "mealie_get_organizers_tools_item_id",
            "mealie_get_organizers_tools_slug_tool_slug",
            "mealie_post_organizers_tools",
            "mealie_put_organizers_tools_item_id",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-curator",
        ),
        skills=("mealie-organizer-operations",),
    ),
    SurfaceLink(
        "mealie-manage-tag",
        tools=(
            "mealie_delete_recipe_tag",
            "mealie_get_empty_tags",
            "mealie_get_organizers_tags",
            "mealie_get_organizers_tags_item_id",
            "mealie_get_organizers_tags_slug_tag_slug",
            "mealie_post_organizers_tags",
            "mealie_put_organizers_tags_item_id",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-curator",
        ),
        skills=("mealie-organizer-operations",),
    ),
    SurfaceLink(
        "mealie-inspect-organizer",
        tools=("mealie_get_all_empty",),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-curator",
        ),
        skills=("mealie-organizer-operations",),
    ),
    SurfaceLink(
        "mealie-manage-shared-recipe",
        tools=(
            "mealie_delete_shared_recipes_item_id",
            "mealie_get_shared_recipe",
            "mealie_get_shared_recipe_as_zip",
            "mealie_get_shared_recipes",
            "mealie_get_shared_recipes_item_id",
            "mealie_post_shared_recipes",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-curator",
        ),
        skills=("mealie-shared-recipes",),
    ),
    SurfaceLink(
        "mealie-manage-shopping",
        tools=(
            "mealie_add_recipe_ingredients_to_list",
            "mealie_add_single_recipe_ingredients_to_list",
            "mealie_delete_households_shopping_items",
            "mealie_delete_households_shopping_items_item_id",
            "mealie_delete_households_shopping_lists_item_id",
            "mealie_get_households_shopping_items",
            "mealie_get_households_shopping_items_item_id",
            "mealie_get_households_shopping_lists",
            "mealie_get_households_shopping_lists_item_id",
            "mealie_post_households_shopping_items",
            "mealie_post_households_shopping_items_create_bulk",
            "mealie_post_households_shopping_lists",
            "mealie_put_households_shopping_items",
            "mealie_put_households_shopping_items_item_id",
            "mealie_put_households_shopping_lists_item_id",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-meal-planner",
        ),
        skills=("mealie-household-planning",),
    ),
    SurfaceLink(
        "mealie-manage-household",
        tools=(
            "mealie_create_invite_token",
            "mealie_email_invitation",
            "mealie_get_group_member",
            "mealie_get_group_members",
            "mealie_get_group_preferences",
            "mealie_get_household",
            "mealie_get_household_members",
            "mealie_get_household_preferences",
            "mealie_get_household_recipe",
            "mealie_get_invite_tokens",
            "mealie_get_logged_in_user_group",
            "mealie_get_logged_in_user_household",
            "mealie_get_one_household",
            "mealie_get_statistics",
            "mealie_set_member_permissions",
            "mealie_update_group_preferences",
            "mealie_update_household_preferences",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-meal-planner",
        ),
        skills=("mealie-household-planning",),
    ),
    SurfaceLink(
        "mealie-manage-mealplan",
        tools=(
            "mealie_create_random_meal",
            "mealie_delete_households_mealplans_item_id",
            "mealie_delete_households_mealplans_rules_item_id",
            "mealie_get_households_mealplans",
            "mealie_get_households_mealplans_item_id",
            "mealie_get_households_mealplans_rules",
            "mealie_get_households_mealplans_rules_item_id",
            "mealie_get_todays_meals",
            "mealie_post_households_mealplans",
            "mealie_post_households_mealplans_rules",
            "mealie_put_households_mealplans_item_id",
            "mealie_put_households_mealplans_rules_item_id",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-meal-planner",
        ),
        skills=("mealie-household-planning",),
    ),
    SurfaceLink(
        "mealie-manage-label",
        tools=(
            "mealie_delete_groups_labels_item_id",
            "mealie_get_groups_labels",
            "mealie_get_groups_labels_item_id",
            "mealie_post_groups_labels",
            "mealie_put_groups_labels_item_id",
            "mealie_seed_labels",
            "mealie_update_label_settings",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-meal-planner",
        ),
        skills=("mealie-household-planning",),
    ),
    SurfaceLink(
        "mealie-manage-report",
        tools=(
            "mealie_delete_groups_reports_item_id",
            "mealie_get_groups_reports",
            "mealie_get_groups_reports_item_id",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-meal-planner",
        ),
        skills=("mealie-household-planning",),
    ),
    SurfaceLink(
        "mealie-manage-cookbook",
        tools=(
            "mealie_delete_households_cookbooks_item_id",
            "mealie_get_households_cookbooks",
            "mealie_get_households_cookbooks_item_id",
            "mealie_post_households_cookbooks",
            "mealie_put_households_cookbooks",
            "mealie_put_households_cookbooks_item_id",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-meal-planner",
        ),
        skills=("mealie-household-planning",),
    ),
    SurfaceLink(
        "mealie-manage-automation",
        tools=(
            "mealie_delete_households_events_notifications_item_id",
            "mealie_delete_households_recipe_actions_item_id",
            "mealie_delete_households_webhooks_item_id",
            "mealie_get_households_events_notifications",
            "mealie_get_households_events_notifications_item_id",
            "mealie_get_households_recipe_actions",
            "mealie_get_households_recipe_actions_item_id",
            "mealie_get_households_webhooks",
            "mealie_get_households_webhooks_item_id",
            "mealie_post_households_events_notifications",
            "mealie_post_households_recipe_actions",
            "mealie_post_households_webhooks",
            "mealie_put_households_events_notifications_item_id",
            "mealie_put_households_recipe_actions_item_id",
            "mealie_put_households_webhooks_item_id",
            "mealie_rerun_webhooks",
            "mealie_test_notification",
            "mealie_test_one",
            "mealie_trigger_action",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-meal-planner",
        ),
        skills=("mealie-household-planning",),
    ),
    SurfaceLink(
        "mealie-manage-food",
        tools=(
            "mealie_delete_foods_item_id",
            "mealie_get_foods",
            "mealie_get_foods_item_id",
            "mealie_post_foods",
            "mealie_put_foods_item_id",
            "mealie_put_foods_merge",
            "mealie_recipe_food_create",
            "mealie_recipe_foods",
            "mealie_seed_foods",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-curator",
        ),
        skills=("mealie-foods-and-units",),
    ),
    SurfaceLink(
        "mealie-manage-unit",
        tools=(
            "mealie_delete_units_item_id",
            "mealie_get_units",
            "mealie_get_units_item_id",
            "mealie_post_units",
            "mealie_put_units_item_id",
            "mealie_put_units_merge",
            "mealie_recipe_unit_create",
            "mealie_recipe_units",
            "mealie_seed_units",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-curator",
        ),
        skills=("mealie-foods-and-units",),
    ),
    SurfaceLink(
        "mealie-inspect-parser",
        tools=(
            "mealie_parse_ingredient",
            "mealie_parse_ingredients",
            "mealie_post_parser_ingredient",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-curator",
        ),
        skills=("mealie-foods-and-units",),
    ),
    SurfaceLink(
        "mealie-manage-recipe-bulk",
        tools=(
            "mealie_bulk_categorize_recipes",
            "mealie_bulk_delete_recipes",
            "mealie_bulk_export_recipes",
            "mealie_bulk_settings_recipes",
            "mealie_bulk_tag_recipes",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-curator",
        ),
        skills=("mealie-recipe-operations",),
    ),
    SurfaceLink(
        "mealie-manage-recipe-import",
        tools=(
            "mealie_create_recipe_from_html_or_json",
            "mealie_create_recipe_from_image",
            "mealie_create_recipe_from_zip",
            "mealie_import_one",
            "mealie_ingest_recipes",
            "mealie_parse_recipe_url",
            "mealie_parse_recipe_url_bulk",
            "mealie_scrape_image_url",
            "mealie_start_data_migration",
            "mealie_test_parse_recipe_url",
            "mealie_upload_one",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-curator",
        ),
        skills=("mealie-recipe-operations",),
    ),
    SurfaceLink(
        "mealie-manage-recipe-media",
        tools=(
            "mealie_delete_recipe_image",
            "mealie_get_recipe_as_format",
            "mealie_get_recipe_asset",
            "mealie_get_recipe_formats_and_templates",
            "mealie_get_recipe_img",
            "mealie_get_recipe_timeline_event_img",
            "mealie_update_event_image",
            "mealie_update_recipe_image",
            "mealie_upload_recipe_asset",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-curator",
        ),
        skills=("mealie-recipe-operations",),
    ),
    SurfaceLink(
        "mealie-manage-recipe",
        tools=(
            "mealie_delete_recipes_slug",
            "mealie_duplicate_one",
            "mealie_get_recipe",
            "mealie_get_recipes",
            "mealie_get_recipes_slug",
            "mealie_get_recipes_suggestions",
            "mealie_patch_many",
            "mealie_patch_one",
            "mealie_post_recipes",
            "mealie_put_recipes",
            "mealie_put_recipes_slug",
            "mealie_recipe_create",
            "mealie_recipe_patch",
            "mealie_recipe_update",
            "mealie_remove_recipe_ingredients_from_list",
            "mealie_unlock_users",
            "mealie_update_last_made",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-curator",
        ),
        skills=("mealie-recipe-operations",),
    ),
    SurfaceLink(
        "mealie-manage-recipe-timeline",
        tools=(
            "mealie_delete_recipes_timeline_events_item_id",
            "mealie_get_recipes_timeline_events",
            "mealie_get_recipes_timeline_events_item_id",
            "mealie_post_recipes_timeline_events",
            "mealie_put_recipes_timeline_events_item_id",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-curator",
        ),
        skills=("mealie-recipe-operations",),
    ),
    SurfaceLink(
        "mealie-manage-recipe-comment",
        tools=(
            "mealie_get_comments",
            "mealie_get_comments_item_id",
            "mealie_get_recipe_comments",
            "mealie_post_comments",
            "mealie_put_comments_item_id",
        ),
        prompts=(
            "culinary_specialist",
            "mealie-recipe-curator",
        ),
        skills=("mealie-recipe-operations",),
    ),
    SurfaceLink(
        "mealie-mcp-operations",
        tools=(
            "mealie_get_app_info",
            "mealie_get_recipes",
        ),
        prompts=("culinary_specialist",),
        skills=("mealie-mcp-operations",),
    ),
    SurfaceLink(
        "mealie-meal-planning",
        tools=(
            "mealie_get_households_mealplans",
            "mealie_post_households_mealplans",
        ),
        prompts=("culinary_specialist",),
        skills=("mealie-meal-planning",),
    ),
    SurfaceLink(
        "mealie-organizer-catalog",
        tools=(
            "mealie_get_organizers_categories",
            "mealie_get_organizers_tags",
        ),
        prompts=("culinary_specialist",),
        skills=("mealie-organizer-catalog",),
    ),
    SurfaceLink(
        "mealie-recipe-management",
        tools=(
            "mealie_ingest_recipes",
            "mealie_recipe_create",
            "mealie_recipe_food_create",
            "mealie_recipe_foods",
            "mealie_recipe_patch",
            "mealie_recipe_unit_create",
            "mealie_recipe_units",
            "mealie_recipe_update",
        ),
        prompts=("culinary_specialist",),
        skills=("mealie-recipe-management",),
    ),
)

LOCATIONS = (
    DataLocation(
        "mealie-recipes",
        ("Recipe",),
        "MEALIE_BASE_URL",
        "mealie_get_recipes",
    ),
    DataLocation(
        "mealie-mealplans",
        ("MealPlan",),
        "MEALIE_BASE_URL",
        "mealie_get_households_mealplans",
    ),
    DataLocation(
        "mealie-shopping",
        ("ShoppingList",),
        "MEALIE_BASE_URL",
        "mealie_get_households_shopping_lists",
    ),
    DataLocation(
        "mealie-cookbooks",
        ("Cookbook",),
        "MEALIE_BASE_URL",
        "mealie_get_households_cookbooks",
    ),
    DataLocation(
        "mealie-categories",
        ("RecipeCategory",),
        "MEALIE_BASE_URL",
        "mealie_get_organizers_categories",
    ),
    DataLocation(
        "mealie-foods",
        ("Food",),
        "MEALIE_BASE_URL",
        "mealie_get_foods",
    ),
    DataLocation(
        "mealie-households",
        ("Household",),
        "MEALIE_BASE_URL",
        "mealie_get_all_households",
    ),
)

ROLES = (
    BusinessRole(
        "recipe curator",
        tasks=(
            "mealie-inspect-organizer",
            "mealie-inspect-parser",
            "mealie-manage-category",
            "mealie-manage-food",
            "mealie-manage-recipe",
            "mealie-manage-recipe-bulk",
            "mealie-manage-recipe-comment",
            "mealie-manage-recipe-import",
            "mealie-manage-recipe-media",
            "mealie-manage-recipe-timeline",
            "mealie-manage-shared-recipe",
            "mealie-manage-tag",
            "mealie-manage-tool",
            "mealie-manage-unit",
        ),
    ),
    BusinessRole(
        "meal planner",
        tasks=(
            "mealie-manage-automation",
            "mealie-manage-cookbook",
            "mealie-manage-household",
            "mealie-manage-label",
            "mealie-manage-mealplan",
            "mealie-manage-report",
            "mealie-manage-shopping",
        ),
    ),
    BusinessRole(
        "household administrator",
        tasks=(
            "mealie-manage-admin-user",
            "mealie-manage-app",
            "mealie-manage-auth",
            "mealie-manage-backup",
            "mealie-manage-group-admin",
            "mealie-manage-maintenance",
            "mealie-manage-profile",
            "mealie-manage-rating",
        ),
    ),
    BusinessRole(
        "recipe browser",
        tasks=(
            "mealie-inspect-explore-catalog",
            "mealie-inspect-explore-organizer",
            "mealie-inspect-explore-recipe",
        ),
    ),
)
