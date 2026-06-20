#!/usr/bin/python
import warnings

from agent_utilities.mcp_utilities import load_config, resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import os
import sys
from typing import Any

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_server
from starlette.requests import Request
from starlette.responses import JSONResponse

from mealie_mcp.auth import get_client

__version__ = "0.42.0"

logger = get_logger(name="mealie-mcp")
logger.setLevel(logging.INFO)


VALID_APP_ACTIONS = (
    "get_startup_info",
    "get_app_theme",
)


def register_app_tools(mcp: FastMCP):
    @mcp.tool(tags={"app"})
    async def mealie_app(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_startup_info', 'get_app_theme'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage mealie app operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, VALID_APP_ACTIONS, service="mealie-mcp")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_startup_info":
            return await run_blocking(client.get_startup_info, **kwargs)
        if action == "get_app_theme":
            return await run_blocking(client.get_app_theme, **kwargs)
        raise ValueError(f"Unknown action: {action}")


VALID_USERS_ACTIONS = (
    "get_token",
    "oauth_login",
    "oauth_callback",
    "refresh_token",
    "logout",
    "register_new_user",
    "get_logged_in_user",
    "get_logged_in_user_ratings",
    "get_logged_in_user_rating_for_recipe",
    "get_logged_in_user_favorites",
    "update_password",
    "update_user",
    "forgot_password",
    "reset_password",
    "update_user_image",
    "create",
    "delete",
    "get_ratings",
    "get_favorites",
    "set_rating",
    "add_favorite",
    "remove_favorite",
)


def register_users_tools(mcp: FastMCP):
    @mcp.tool(tags={"users"})
    async def mealie_users(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_token', 'oauth_login', 'oauth_callback', 'refresh_token', 'logout', 'register_new_user', 'get_logged_in_user', 'get_logged_in_user_ratings', 'get_logged_in_user_rating_for_recipe', 'get_logged_in_user_favorites', 'update_password', 'update_user', 'forgot_password', 'reset_password', 'update_user_image', 'create', 'delete', 'get_ratings', 'get_favorites', 'set_rating', 'add_favorite', 'remove_favorite'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage mealie users operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, VALID_USERS_ACTIONS, service="mealie-mcp")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_token":
            return await run_blocking(client.get_token, **kwargs)
        if action == "oauth_login":
            return await run_blocking(client.oauth_login, **kwargs)
        if action == "oauth_callback":
            return await run_blocking(client.oauth_callback, **kwargs)
        if action == "refresh_token":
            return await run_blocking(client.refresh_token, **kwargs)
        if action == "logout":
            return await run_blocking(client.logout, **kwargs)
        if action == "register_new_user":
            return await run_blocking(client.register_new_user, **kwargs)
        if action == "get_logged_in_user":
            return await run_blocking(client.get_logged_in_user, **kwargs)
        if action == "get_logged_in_user_ratings":
            return await run_blocking(client.get_logged_in_user_ratings, **kwargs)
        if action == "get_logged_in_user_rating_for_recipe":
            return await run_blocking(
                client.get_logged_in_user_rating_for_recipe, **kwargs
            )
        if action == "get_logged_in_user_favorites":
            return await run_blocking(client.get_logged_in_user_favorites, **kwargs)
        if action == "update_password":
            return await run_blocking(client.update_password, **kwargs)
        if action == "update_user":
            return await run_blocking(client.update_user, **kwargs)
        if action == "forgot_password":
            return await run_blocking(client.forgot_password, **kwargs)
        if action == "reset_password":
            return await run_blocking(client.reset_password, **kwargs)
        if action == "update_user_image":
            return await run_blocking(client.update_user_image, **kwargs)
        if action == "create":
            return await run_blocking(client.create, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete, **kwargs)
        if action == "get_ratings":
            return await run_blocking(client.get_ratings, **kwargs)
        if action == "get_favorites":
            return await run_blocking(client.get_favorites, **kwargs)
        if action == "set_rating":
            return await run_blocking(client.set_rating, **kwargs)
        if action == "add_favorite":
            return await run_blocking(client.add_favorite, **kwargs)
        if action == "remove_favorite":
            return await run_blocking(client.remove_favorite, **kwargs)
        raise ValueError(f"Unknown action: {action}")


VALID_HOUSEHOLDS_ACTIONS = (
    "get_households_cookbooks",
    "post_households_cookbooks",
    "put_households_cookbooks",
    "get_households_cookbooks_item_id",
    "put_households_cookbooks_item_id",
    "delete_households_cookbooks_item_id",
    "get_households_events_notifications",
    "post_households_events_notifications",
    "get_households_events_notifications_item_id",
    "put_households_events_notifications_item_id",
    "delete_households_events_notifications_item_id",
    "test_notification",
    "get_households_recipe_actions",
    "post_households_recipe_actions",
    "get_households_recipe_actions_item_id",
    "put_households_recipe_actions_item_id",
    "delete_households_recipe_actions_item_id",
    "trigger_action",
    "get_logged_in_user_household",
    "get_household_recipe",
    "get_household_members",
    "get_household_preferences",
    "update_household_preferences",
    "set_member_permissions",
    "get_statistics",
    "get_invite_tokens",
    "create_invite_token",
    "email_invitation",
    "get_households_shopping_lists",
    "post_households_shopping_lists",
    "get_households_shopping_lists_item_id",
    "put_households_shopping_lists_item_id",
    "delete_households_shopping_lists_item_id",
    "update_label_settings",
    "add_recipe_ingredients_to_list",
    "add_single_recipe_ingredients_to_list",
    "remove_recipe_ingredients_from_list",
    "get_households_shopping_items",
    "post_households_shopping_items",
    "put_households_shopping_items",
    "delete_households_shopping_items",
    "post_households_shopping_items_create_bulk",
    "get_households_shopping_items_item_id",
    "put_households_shopping_items_item_id",
    "delete_households_shopping_items_item_id",
    "get_households_webhooks",
    "post_households_webhooks",
    "rerun_webhooks",
    "get_households_webhooks_item_id",
    "put_households_webhooks_item_id",
    "delete_households_webhooks_item_id",
    "test_one",
    "get_households_mealplans_rules",
    "post_households_mealplans_rules",
    "get_households_mealplans_rules_item_id",
    "put_households_mealplans_rules_item_id",
    "delete_households_mealplans_rules_item_id",
    "get_households_mealplans",
    "post_households_mealplans",
    "get_todays_meals",
    "create_random_meal",
    "get_households_mealplans_item_id",
    "put_households_mealplans_item_id",
    "delete_households_mealplans_item_id",
)


def register_households_tools(mcp: FastMCP):
    @mcp.tool(tags={"households"})
    async def mealie_households(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_households_cookbooks', 'post_households_cookbooks', 'put_households_cookbooks', 'get_households_cookbooks_item_id', 'put_households_cookbooks_item_id', 'delete_households_cookbooks_item_id', 'get_households_events_notifications', 'post_households_events_notifications', 'get_households_events_notifications_item_id', 'put_households_events_notifications_item_id', 'delete_households_events_notifications_item_id', 'test_notification', 'get_households_recipe_actions', 'post_households_recipe_actions', 'get_households_recipe_actions_item_id', 'put_households_recipe_actions_item_id', 'delete_households_recipe_actions_item_id', 'trigger_action', 'get_logged_in_user_household', 'get_household_recipe', 'get_household_members', 'get_household_preferences', 'update_household_preferences', 'set_member_permissions', 'get_statistics', 'get_invite_tokens', 'create_invite_token', 'email_invitation', 'get_households_shopping_lists', 'post_households_shopping_lists', 'get_households_shopping_lists_item_id', 'put_households_shopping_lists_item_id', 'delete_households_shopping_lists_item_id', 'update_label_settings', 'add_recipe_ingredients_to_list', 'add_single_recipe_ingredients_to_list', 'remove_recipe_ingredients_from_list', 'get_households_shopping_items', 'post_households_shopping_items', 'put_households_shopping_items', 'delete_households_shopping_items', 'post_households_shopping_items_create_bulk', 'get_households_shopping_items_item_id', 'put_households_shopping_items_item_id', 'delete_households_shopping_items_item_id', 'get_households_webhooks', 'post_households_webhooks', 'rerun_webhooks', 'get_households_webhooks_item_id', 'put_households_webhooks_item_id', 'delete_households_webhooks_item_id', 'test_one', 'get_households_mealplans_rules', 'post_households_mealplans_rules', 'get_households_mealplans_rules_item_id', 'put_households_mealplans_rules_item_id', 'delete_households_mealplans_rules_item_id', 'get_households_mealplans', 'post_households_mealplans', 'get_todays_meals', 'create_random_meal', 'get_households_mealplans_item_id', 'put_households_mealplans_item_id', 'delete_households_mealplans_item_id'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage mealie households operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, VALID_HOUSEHOLDS_ACTIONS, service="mealie-mcp"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_households_cookbooks":
            return await run_blocking(client.get_households_cookbooks, **kwargs)
        if action == "post_households_cookbooks":
            return await run_blocking(client.post_households_cookbooks, **kwargs)
        if action == "put_households_cookbooks":
            return await run_blocking(client.put_households_cookbooks, **kwargs)
        if action == "get_households_cookbooks_item_id":
            return await run_blocking(client.get_households_cookbooks_item_id, **kwargs)
        if action == "put_households_cookbooks_item_id":
            return await run_blocking(client.put_households_cookbooks_item_id, **kwargs)
        if action == "delete_households_cookbooks_item_id":
            return await run_blocking(
                client.delete_households_cookbooks_item_id, **kwargs
            )
        if action == "get_households_events_notifications":
            return await run_blocking(
                client.get_households_events_notifications, **kwargs
            )
        if action == "post_households_events_notifications":
            return await run_blocking(
                client.post_households_events_notifications, **kwargs
            )
        if action == "get_households_events_notifications_item_id":
            return await run_blocking(
                client.get_households_events_notifications_item_id, **kwargs
            )
        if action == "put_households_events_notifications_item_id":
            return await run_blocking(
                client.put_households_events_notifications_item_id, **kwargs
            )
        if action == "delete_households_events_notifications_item_id":
            return await run_blocking(
                client.delete_households_events_notifications_item_id, **kwargs
            )
        if action == "test_notification":
            return await run_blocking(client.test_notification, **kwargs)
        if action == "get_households_recipe_actions":
            return await run_blocking(client.get_households_recipe_actions, **kwargs)
        if action == "post_households_recipe_actions":
            return await run_blocking(client.post_households_recipe_actions, **kwargs)
        if action == "get_households_recipe_actions_item_id":
            return await run_blocking(
                client.get_households_recipe_actions_item_id, **kwargs
            )
        if action == "put_households_recipe_actions_item_id":
            return await run_blocking(
                client.put_households_recipe_actions_item_id, **kwargs
            )
        if action == "delete_households_recipe_actions_item_id":
            return await run_blocking(
                client.delete_households_recipe_actions_item_id, **kwargs
            )
        if action == "trigger_action":
            return await run_blocking(client.trigger_action, **kwargs)
        if action == "get_logged_in_user_household":
            return await run_blocking(client.get_logged_in_user_household, **kwargs)
        if action == "get_household_recipe":
            return await run_blocking(client.get_household_recipe, **kwargs)
        if action == "get_household_members":
            return await run_blocking(client.get_household_members, **kwargs)
        if action == "get_household_preferences":
            return await run_blocking(client.get_household_preferences, **kwargs)
        if action == "update_household_preferences":
            return await run_blocking(client.update_household_preferences, **kwargs)
        if action == "set_member_permissions":
            return await run_blocking(client.set_member_permissions, **kwargs)
        if action == "get_statistics":
            return await run_blocking(client.get_statistics, **kwargs)
        if action == "get_invite_tokens":
            return await run_blocking(client.get_invite_tokens, **kwargs)
        if action == "create_invite_token":
            return await run_blocking(client.create_invite_token, **kwargs)
        if action == "email_invitation":
            return await run_blocking(client.email_invitation, **kwargs)
        if action == "get_households_shopping_lists":
            return await run_blocking(client.get_households_shopping_lists, **kwargs)
        if action == "post_households_shopping_lists":
            return await run_blocking(client.post_households_shopping_lists, **kwargs)
        if action == "get_households_shopping_lists_item_id":
            return await run_blocking(
                client.get_households_shopping_lists_item_id, **kwargs
            )
        if action == "put_households_shopping_lists_item_id":
            return await run_blocking(
                client.put_households_shopping_lists_item_id, **kwargs
            )
        if action == "delete_households_shopping_lists_item_id":
            return await run_blocking(
                client.delete_households_shopping_lists_item_id, **kwargs
            )
        if action == "update_label_settings":
            return await run_blocking(client.update_label_settings, **kwargs)
        if action == "add_recipe_ingredients_to_list":
            return await run_blocking(client.add_recipe_ingredients_to_list, **kwargs)
        if action == "add_single_recipe_ingredients_to_list":
            return await run_blocking(
                client.add_single_recipe_ingredients_to_list, **kwargs
            )
        if action == "remove_recipe_ingredients_from_list":
            return await run_blocking(
                client.remove_recipe_ingredients_from_list, **kwargs
            )
        if action == "get_households_shopping_items":
            return await run_blocking(client.get_households_shopping_items, **kwargs)
        if action == "post_households_shopping_items":
            return await run_blocking(client.post_households_shopping_items, **kwargs)
        if action == "put_households_shopping_items":
            return await run_blocking(client.put_households_shopping_items, **kwargs)
        if action == "delete_households_shopping_items":
            return await run_blocking(client.delete_households_shopping_items, **kwargs)
        if action == "post_households_shopping_items_create_bulk":
            return await run_blocking(
                client.post_households_shopping_items_create_bulk, **kwargs
            )
        if action == "get_households_shopping_items_item_id":
            return await run_blocking(
                client.get_households_shopping_items_item_id, **kwargs
            )
        if action == "put_households_shopping_items_item_id":
            return await run_blocking(
                client.put_households_shopping_items_item_id, **kwargs
            )
        if action == "delete_households_shopping_items_item_id":
            return await run_blocking(
                client.delete_households_shopping_items_item_id, **kwargs
            )
        if action == "get_households_webhooks":
            return await run_blocking(client.get_households_webhooks, **kwargs)
        if action == "post_households_webhooks":
            return await run_blocking(client.post_households_webhooks, **kwargs)
        if action == "rerun_webhooks":
            return await run_blocking(client.rerun_webhooks, **kwargs)
        if action == "get_households_webhooks_item_id":
            return await run_blocking(client.get_households_webhooks_item_id, **kwargs)
        if action == "put_households_webhooks_item_id":
            return await run_blocking(client.put_households_webhooks_item_id, **kwargs)
        if action == "delete_households_webhooks_item_id":
            return await run_blocking(
                client.delete_households_webhooks_item_id, **kwargs
            )
        if action == "test_one":
            return await run_blocking(client.test_one, **kwargs)
        if action == "get_households_mealplans_rules":
            return await run_blocking(client.get_households_mealplans_rules, **kwargs)
        if action == "post_households_mealplans_rules":
            return await run_blocking(client.post_households_mealplans_rules, **kwargs)
        if action == "get_households_mealplans_rules_item_id":
            return await run_blocking(
                client.get_households_mealplans_rules_item_id, **kwargs
            )
        if action == "put_households_mealplans_rules_item_id":
            return await run_blocking(
                client.put_households_mealplans_rules_item_id, **kwargs
            )
        if action == "delete_households_mealplans_rules_item_id":
            return await run_blocking(
                client.delete_households_mealplans_rules_item_id, **kwargs
            )
        if action == "get_households_mealplans":
            return await run_blocking(client.get_households_mealplans, **kwargs)
        if action == "post_households_mealplans":
            return await run_blocking(client.post_households_mealplans, **kwargs)
        if action == "get_todays_meals":
            return await run_blocking(client.get_todays_meals, **kwargs)
        if action == "create_random_meal":
            return await run_blocking(client.create_random_meal, **kwargs)
        if action == "get_households_mealplans_item_id":
            return await run_blocking(client.get_households_mealplans_item_id, **kwargs)
        if action == "put_households_mealplans_item_id":
            return await run_blocking(client.put_households_mealplans_item_id, **kwargs)
        if action == "delete_households_mealplans_item_id":
            return await run_blocking(
                client.delete_households_mealplans_item_id, **kwargs
            )
        raise ValueError(f"Unknown action: {action}")


VALID_GROUPS_ACTIONS = (
    "get_all_households",
    "get_one_household",
    "get_logged_in_user_group",
    "get_group_members",
    "get_group_member",
    "get_group_preferences",
    "update_group_preferences",
    "get_storage",
    "start_data_migration",
    "get_groups_reports",
    "get_groups_reports_item_id",
    "delete_groups_reports_item_id",
    "get_groups_labels",
    "post_groups_labels",
    "get_groups_labels_item_id",
    "put_groups_labels_item_id",
    "delete_groups_labels_item_id",
    "seed_foods",
    "seed_labels",
    "seed_units",
)


def register_groups_tools(mcp: FastMCP):
    @mcp.tool(tags={"groups"})
    async def mealie_groups(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_all_households', 'get_one_household', 'get_logged_in_user_group', 'get_group_members', 'get_group_member', 'get_group_preferences', 'update_group_preferences', 'get_storage', 'start_data_migration', 'get_groups_reports', 'get_groups_reports_item_id', 'delete_groups_reports_item_id', 'get_groups_labels', 'post_groups_labels', 'get_groups_labels_item_id', 'put_groups_labels_item_id', 'delete_groups_labels_item_id', 'seed_foods', 'seed_labels', 'seed_units'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage mealie groups operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, VALID_GROUPS_ACTIONS, service="mealie-mcp")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_all_households":
            return await run_blocking(client.get_all_households, **kwargs)
        if action == "get_one_household":
            return await run_blocking(client.get_one_household, **kwargs)
        if action == "get_logged_in_user_group":
            return await run_blocking(client.get_logged_in_user_group, **kwargs)
        if action == "get_group_members":
            return await run_blocking(client.get_group_members, **kwargs)
        if action == "get_group_member":
            return await run_blocking(client.get_group_member, **kwargs)
        if action == "get_group_preferences":
            return await run_blocking(client.get_group_preferences, **kwargs)
        if action == "update_group_preferences":
            return await run_blocking(client.update_group_preferences, **kwargs)
        if action == "get_storage":
            return await run_blocking(client.get_storage, **kwargs)
        if action == "start_data_migration":
            return await run_blocking(client.start_data_migration, **kwargs)
        if action == "get_groups_reports":
            return await run_blocking(client.get_groups_reports, **kwargs)
        if action == "get_groups_reports_item_id":
            return await run_blocking(client.get_groups_reports_item_id, **kwargs)
        if action == "delete_groups_reports_item_id":
            return await run_blocking(client.delete_groups_reports_item_id, **kwargs)
        if action == "get_groups_labels":
            return await run_blocking(client.get_groups_labels, **kwargs)
        if action == "post_groups_labels":
            return await run_blocking(client.post_groups_labels, **kwargs)
        if action == "get_groups_labels_item_id":
            return await run_blocking(client.get_groups_labels_item_id, **kwargs)
        if action == "put_groups_labels_item_id":
            return await run_blocking(client.put_groups_labels_item_id, **kwargs)
        if action == "delete_groups_labels_item_id":
            return await run_blocking(client.delete_groups_labels_item_id, **kwargs)
        if action == "seed_foods":
            return await run_blocking(client.seed_foods, **kwargs)
        if action == "seed_labels":
            return await run_blocking(client.seed_labels, **kwargs)
        if action == "seed_units":
            return await run_blocking(client.seed_units, **kwargs)
        raise ValueError(f"Unknown action: {action}")


VALID_RECIPES_ACTIONS = (
    "get_recipe_formats_and_templates",
    "get_recipe_as_format",
    "test_parse_recipe_url",
    "create_recipe_from_html_or_json",
    "parse_recipe_url",
    "parse_recipe_url_bulk",
    "create_recipe_from_zip",
    "create_recipe_from_image",
    "get_recipes",
    "post_recipes",
    "put_recipes",
    "patch_many",
    "get_recipes_suggestions",
    "get_recipes_slug",
    "put_recipes_slug",
    "patch_one",
    "delete_recipes_slug",
    "duplicate_one",
    "update_last_made",
    "scrape_image_url",
    "update_recipe_image",
    "delete_recipe_image",
    "upload_recipe_asset",
    "get_recipe_comments",
    "bulk_tag_recipes",
    "bulk_settings_recipes",
    "bulk_categorize_recipes",
    "bulk_delete_recipes",
    "bulk_export_recipes",
    "get_exported_data",
    "get_exported_data_token",
    "purge_export_data",
    "get_shared_recipe",
    "get_shared_recipe_as_zip",
    "get_recipes_timeline_events",
    "post_recipes_timeline_events",
    "get_recipes_timeline_events_item_id",
    "put_recipes_timeline_events_item_id",
    "delete_recipes_timeline_events_item_id",
    "update_event_image",
    "get_comments",
    "post_comments",
    "get_comments_item_id",
    "put_comments_item_id",
    "post_parser_ingredient",
    "parse_ingredient",
    "parse_ingredients",
    "get_foods",
    "post_foods",
    "put_foods_merge",
    "get_foods_item_id",
    "put_foods_item_id",
    "delete_foods_item_id",
    "get_units",
    "post_units",
    "put_units_merge",
    "get_units_item_id",
    "put_units_item_id",
    "delete_units_item_id",
    "get_recipe_img",
    "get_recipe_timeline_event_img",
    "get_recipe_asset",
    "get_user_image",
    "get_validation_text",
)


def register_recipes_tools(mcp: FastMCP):
    @mcp.tool(tags={"recipes"})
    async def mealie_recipes(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_recipe_formats_and_templates', 'get_recipe_as_format', 'test_parse_recipe_url', 'create_recipe_from_html_or_json', 'parse_recipe_url', 'parse_recipe_url_bulk', 'create_recipe_from_zip', 'create_recipe_from_image', 'get_recipes', 'post_recipes', 'put_recipes', 'patch_many', 'get_recipes_suggestions', 'get_recipes_slug', 'put_recipes_slug', 'patch_one', 'delete_recipes_slug', 'duplicate_one', 'update_last_made', 'scrape_image_url', 'update_recipe_image', 'delete_recipe_image', 'upload_recipe_asset', 'get_recipe_comments', 'bulk_tag_recipes', 'bulk_settings_recipes', 'bulk_categorize_recipes', 'bulk_delete_recipes', 'bulk_export_recipes', 'get_exported_data', 'get_exported_data_token', 'purge_export_data', 'get_shared_recipe', 'get_shared_recipe_as_zip', 'get_recipes_timeline_events', 'post_recipes_timeline_events', 'get_recipes_timeline_events_item_id', 'put_recipes_timeline_events_item_id', 'delete_recipes_timeline_events_item_id', 'update_event_image', 'get_comments', 'post_comments', 'get_comments_item_id', 'put_comments_item_id', 'post_parser_ingredient', 'parse_ingredient', 'parse_ingredients', 'get_foods', 'post_foods', 'put_foods_merge', 'get_foods_item_id', 'put_foods_item_id', 'delete_foods_item_id', 'get_units', 'post_units', 'put_units_merge', 'get_units_item_id', 'put_units_item_id', 'delete_units_item_id', 'get_recipe_img', 'get_recipe_timeline_event_img', 'get_recipe_asset', 'get_user_image', 'get_validation_text'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage mealie recipes operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, VALID_RECIPES_ACTIONS, service="mealie-mcp")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_recipe_formats_and_templates":
            return await run_blocking(client.get_recipe_formats_and_templates, **kwargs)
        if action == "get_recipe_as_format":
            return await run_blocking(client.get_recipe_as_format, **kwargs)
        if action == "test_parse_recipe_url":
            return await run_blocking(client.test_parse_recipe_url, **kwargs)
        if action == "create_recipe_from_html_or_json":
            return await run_blocking(client.create_recipe_from_html_or_json, **kwargs)
        if action == "parse_recipe_url":
            return await run_blocking(client.parse_recipe_url, **kwargs)
        if action == "parse_recipe_url_bulk":
            return await run_blocking(client.parse_recipe_url_bulk, **kwargs)
        if action == "create_recipe_from_zip":
            return await run_blocking(client.create_recipe_from_zip, **kwargs)
        if action == "create_recipe_from_image":
            return await run_blocking(client.create_recipe_from_image, **kwargs)
        if action == "get_recipes":
            return await run_blocking(client.get_recipes, **kwargs)
        if action == "post_recipes":
            return await run_blocking(client.post_recipes, **kwargs)
        if action == "put_recipes":
            return await run_blocking(client.put_recipes, **kwargs)
        if action == "patch_many":
            return await run_blocking(client.patch_many, **kwargs)
        if action == "get_recipes_suggestions":
            return await run_blocking(client.get_recipes_suggestions, **kwargs)
        if action == "get_recipes_slug":
            return await run_blocking(client.get_recipes_slug, **kwargs)
        if action == "put_recipes_slug":
            return await run_blocking(client.put_recipes_slug, **kwargs)
        if action == "patch_one":
            return await run_blocking(client.patch_one, **kwargs)
        if action == "delete_recipes_slug":
            return await run_blocking(client.delete_recipes_slug, **kwargs)
        if action == "duplicate_one":
            return await run_blocking(client.duplicate_one, **kwargs)
        if action == "update_last_made":
            return await run_blocking(client.update_last_made, **kwargs)
        if action == "scrape_image_url":
            return await run_blocking(client.scrape_image_url, **kwargs)
        if action == "update_recipe_image":
            return await run_blocking(client.update_recipe_image, **kwargs)
        if action == "delete_recipe_image":
            return await run_blocking(client.delete_recipe_image, **kwargs)
        if action == "upload_recipe_asset":
            return await run_blocking(client.upload_recipe_asset, **kwargs)
        if action == "get_recipe_comments":
            return await run_blocking(client.get_recipe_comments, **kwargs)
        if action == "bulk_tag_recipes":
            return await run_blocking(client.bulk_tag_recipes, **kwargs)
        if action == "bulk_settings_recipes":
            return await run_blocking(client.bulk_settings_recipes, **kwargs)
        if action == "bulk_categorize_recipes":
            return await run_blocking(client.bulk_categorize_recipes, **kwargs)
        if action == "bulk_delete_recipes":
            return await run_blocking(client.bulk_delete_recipes, **kwargs)
        if action == "bulk_export_recipes":
            return await run_blocking(client.bulk_export_recipes, **kwargs)
        if action == "get_exported_data":
            return await run_blocking(client.get_exported_data, **kwargs)
        if action == "get_exported_data_token":
            return await run_blocking(client.get_exported_data_token, **kwargs)
        if action == "purge_export_data":
            return await run_blocking(client.purge_export_data, **kwargs)
        if action == "get_shared_recipe":
            return await run_blocking(client.get_shared_recipe, **kwargs)
        if action == "get_shared_recipe_as_zip":
            return await run_blocking(client.get_shared_recipe_as_zip, **kwargs)
        if action == "get_recipes_timeline_events":
            return await run_blocking(client.get_recipes_timeline_events, **kwargs)
        if action == "post_recipes_timeline_events":
            return await run_blocking(client.post_recipes_timeline_events, **kwargs)
        if action == "get_recipes_timeline_events_item_id":
            return await run_blocking(
                client.get_recipes_timeline_events_item_id, **kwargs
            )
        if action == "put_recipes_timeline_events_item_id":
            return await run_blocking(
                client.put_recipes_timeline_events_item_id, **kwargs
            )
        if action == "delete_recipes_timeline_events_item_id":
            return await run_blocking(
                client.delete_recipes_timeline_events_item_id, **kwargs
            )
        if action == "update_event_image":
            return await run_blocking(client.update_event_image, **kwargs)
        if action == "get_comments":
            return await run_blocking(client.get_comments, **kwargs)
        if action == "post_comments":
            return await run_blocking(client.post_comments, **kwargs)
        if action == "get_comments_item_id":
            return await run_blocking(client.get_comments_item_id, **kwargs)
        if action == "put_comments_item_id":
            return await run_blocking(client.put_comments_item_id, **kwargs)
        if action == "post_parser_ingredient":
            return await run_blocking(client.post_parser_ingredient, **kwargs)
        if action == "parse_ingredient":
            return await run_blocking(client.parse_ingredient, **kwargs)
        if action == "parse_ingredients":
            return await run_blocking(client.parse_ingredients, **kwargs)
        if action == "get_foods":
            return await run_blocking(client.get_foods, **kwargs)
        if action == "post_foods":
            return await run_blocking(client.post_foods, **kwargs)
        if action == "put_foods_merge":
            return await run_blocking(client.put_foods_merge, **kwargs)
        if action == "get_foods_item_id":
            return await run_blocking(client.get_foods_item_id, **kwargs)
        if action == "put_foods_item_id":
            return await run_blocking(client.put_foods_item_id, **kwargs)
        if action == "delete_foods_item_id":
            return await run_blocking(client.delete_foods_item_id, **kwargs)
        if action == "get_units":
            return await run_blocking(client.get_units, **kwargs)
        if action == "post_units":
            return await run_blocking(client.post_units, **kwargs)
        if action == "put_units_merge":
            return await run_blocking(client.put_units_merge, **kwargs)
        if action == "get_units_item_id":
            return await run_blocking(client.get_units_item_id, **kwargs)
        if action == "put_units_item_id":
            return await run_blocking(client.put_units_item_id, **kwargs)
        if action == "delete_units_item_id":
            return await run_blocking(client.delete_units_item_id, **kwargs)
        if action == "get_recipe_img":
            return await run_blocking(client.get_recipe_img, **kwargs)
        if action == "get_recipe_timeline_event_img":
            return await run_blocking(client.get_recipe_timeline_event_img, **kwargs)
        if action == "get_recipe_asset":
            return await run_blocking(client.get_recipe_asset, **kwargs)
        if action == "get_user_image":
            return await run_blocking(client.get_user_image, **kwargs)
        if action == "get_validation_text":
            return await run_blocking(client.get_validation_text, **kwargs)
        raise ValueError(f"Unknown action: {action}")


VALID_ORGANIZER_ACTIONS = (
    "get_organizers_categories",
    "post_organizers_categories",
    "get_all_empty",
    "get_organizers_categories_item_id",
    "put_organizers_categories_item_id",
    "delete_organizers_categories_item_id",
    "get_organizers_categories_slug_category_slug",
    "get_organizers_tags",
    "post_organizers_tags",
    "get_empty_tags",
    "get_organizers_tags_item_id",
    "put_organizers_tags_item_id",
    "delete_recipe_tag",
    "get_organizers_tags_slug_tag_slug",
    "get_organizerss",
    "post_organizerss",
    "get_organizerss_item_id",
    "put_organizerss_item_id",
    "delete_organizerss_item_id",
    "get_organizerss_slug_slug",
)


def register_organizer_tools(mcp: FastMCP):
    @mcp.tool(tags={"organizer"})
    async def mealie_organizer(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_organizers_categories', 'post_organizers_categories', 'get_all_empty', 'get_organizers_categories_item_id', 'put_organizers_categories_item_id', 'delete_organizers_categories_item_id', 'get_organizers_categories_slug_category_slug', 'get_organizers_tags', 'post_organizers_tags', 'get_empty_tags', 'get_organizers_tags_item_id', 'put_organizers_tags_item_id', 'delete_recipe_tag', 'get_organizers_tags_slug_tag_slug', 'get_organizerss', 'post_organizerss', 'get_organizerss_item_id', 'put_organizerss_item_id', 'delete_organizerss_item_id', 'get_organizerss_slug_slug'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage mealie organizer operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, VALID_ORGANIZER_ACTIONS, service="mealie-mcp")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_organizers_categories":
            return await run_blocking(client.get_organizers_categories, **kwargs)
        if action == "post_organizers_categories":
            return await run_blocking(client.post_organizers_categories, **kwargs)
        if action == "get_all_empty":
            return await run_blocking(client.get_all_empty, **kwargs)
        if action == "get_organizers_categories_item_id":
            return await run_blocking(
                client.get_organizers_categories_item_id, **kwargs
            )
        if action == "put_organizers_categories_item_id":
            return await run_blocking(
                client.put_organizers_categories_item_id, **kwargs
            )
        if action == "delete_organizers_categories_item_id":
            return await run_blocking(
                client.delete_organizers_categories_item_id, **kwargs
            )
        if action == "get_organizers_categories_slug_category_slug":
            return await run_blocking(
                client.get_organizers_categories_slug_category_slug, **kwargs
            )
        if action == "get_organizers_tags":
            return await run_blocking(client.get_organizers_tags, **kwargs)
        if action == "post_organizers_tags":
            return await run_blocking(client.post_organizers_tags, **kwargs)
        if action == "get_empty_tags":
            return await run_blocking(client.get_empty_tags, **kwargs)
        if action == "get_organizers_tags_item_id":
            return await run_blocking(client.get_organizers_tags_item_id, **kwargs)
        if action == "put_organizers_tags_item_id":
            return await run_blocking(client.put_organizers_tags_item_id, **kwargs)
        if action == "delete_recipe_tag":
            return await run_blocking(client.delete_recipe_tag, **kwargs)
        if action == "get_organizers_tags_slug_tag_slug":
            return await run_blocking(
                client.get_organizers_tags_slug_tag_slug, **kwargs
            )
        if action == "get_organizerss":
            return await run_blocking(client.get_organizerss, **kwargs)
        if action == "post_organizerss":
            return await run_blocking(client.post_organizerss, **kwargs)
        if action == "get_organizerss_item_id":
            return await run_blocking(client.get_organizerss_item_id, **kwargs)
        if action == "put_organizerss_item_id":
            return await run_blocking(client.put_organizerss_item_id, **kwargs)
        if action == "delete_organizerss_item_id":
            return await run_blocking(client.delete_organizerss_item_id, **kwargs)
        if action == "get_organizerss_slug_slug":
            return await run_blocking(client.get_organizerss_slug_slug, **kwargs)
        raise ValueError(f"Unknown action: {action}")


VALID_SHARED_ACTIONS = (
    "get_shared_recipes",
    "post_shared_recipes",
    "get_shared_recipes_item_id",
    "delete_shared_recipes_item_id",
)


def register_shared_tools(mcp: FastMCP):
    @mcp.tool(tags={"shared"})
    async def mealie_shared(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_shared_recipes', 'post_shared_recipes', 'get_shared_recipes_item_id', 'delete_shared_recipes_item_id'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage mealie shared operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, VALID_SHARED_ACTIONS, service="mealie-mcp")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_shared_recipes":
            return await run_blocking(client.get_shared_recipes, **kwargs)
        if action == "post_shared_recipes":
            return await run_blocking(client.post_shared_recipes, **kwargs)
        if action == "get_shared_recipes_item_id":
            return await run_blocking(client.get_shared_recipes_item_id, **kwargs)
        if action == "delete_shared_recipes_item_id":
            return await run_blocking(client.delete_shared_recipes_item_id, **kwargs)
        raise ValueError(f"Unknown action: {action}")


VALID_ADMIN_ACTIONS = (
    "get_app_info",
    "get_app_statistics",
    "check_app_config",
    "get_admin_users",
    "post_admin_users",
    "unlock_users",
    "get_admin_users_item_id",
    "put_admin_users_item_id",
    "delete_admin_users_item_id",
    "generate_token",
    "get_admin_households",
    "post_admin_households",
    "get_admin_households_item_id",
    "put_admin_households_item_id",
    "delete_admin_households_item_id",
    "get_admin_groups",
    "post_admin_groups",
    "get_admin_groups_item_id",
    "put_admin_groups_item_id",
    "delete_admin_groups_item_id",
    "check_email_config",
    "send_test_email",
    "get_admin_backups",
    "post_admin_backups",
    "get_admin_backups_file_name",
    "delete_admin_backups_file_name",
    "upload_one",
    "import_one",
    "get_maintenance_summary",
    "get_storage_details",
    "clean_images",
    "clean_temp",
    "clean_recipe_folders",
    "debug_openai",
)


def register_admin_tools(mcp: FastMCP):
    @mcp.tool(tags={"admin"})
    async def mealie_admin(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_app_info', 'get_app_statistics', 'check_app_config', 'get_admin_users', 'post_admin_users', 'unlock_users', 'get_admin_users_item_id', 'put_admin_users_item_id', 'delete_admin_users_item_id', 'generate_token', 'get_admin_households', 'post_admin_households', 'get_admin_households_item_id', 'put_admin_households_item_id', 'delete_admin_households_item_id', 'get_admin_groups', 'post_admin_groups', 'get_admin_groups_item_id', 'put_admin_groups_item_id', 'delete_admin_groups_item_id', 'check_email_config', 'send_test_email', 'get_admin_backups', 'post_admin_backups', 'get_admin_backups_file_name', 'delete_admin_backups_file_name', 'upload_one', 'import_one', 'get_maintenance_summary', 'get_storage_details', 'clean_images', 'clean_temp', 'clean_recipe_folders', 'debug_openai'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage mealie admin operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, VALID_ADMIN_ACTIONS, service="mealie-mcp")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_app_info":
            return await run_blocking(client.get_app_info, **kwargs)
        if action == "get_app_statistics":
            return await run_blocking(client.get_app_statistics, **kwargs)
        if action == "check_app_config":
            return await run_blocking(client.check_app_config, **kwargs)
        if action == "get_admin_users":
            return await run_blocking(client.get_admin_users, **kwargs)
        if action == "post_admin_users":
            return await run_blocking(client.post_admin_users, **kwargs)
        if action == "unlock_users":
            return await run_blocking(client.unlock_users, **kwargs)
        if action == "get_admin_users_item_id":
            return await run_blocking(client.get_admin_users_item_id, **kwargs)
        if action == "put_admin_users_item_id":
            return await run_blocking(client.put_admin_users_item_id, **kwargs)
        if action == "delete_admin_users_item_id":
            return await run_blocking(client.delete_admin_users_item_id, **kwargs)
        if action == "generate_token":
            return await run_blocking(client.generate_token, **kwargs)
        if action == "get_admin_households":
            return await run_blocking(client.get_admin_households, **kwargs)
        if action == "post_admin_households":
            return await run_blocking(client.post_admin_households, **kwargs)
        if action == "get_admin_households_item_id":
            return await run_blocking(client.get_admin_households_item_id, **kwargs)
        if action == "put_admin_households_item_id":
            return await run_blocking(client.put_admin_households_item_id, **kwargs)
        if action == "delete_admin_households_item_id":
            return await run_blocking(client.delete_admin_households_item_id, **kwargs)
        if action == "get_admin_groups":
            return await run_blocking(client.get_admin_groups, **kwargs)
        if action == "post_admin_groups":
            return await run_blocking(client.post_admin_groups, **kwargs)
        if action == "get_admin_groups_item_id":
            return await run_blocking(client.get_admin_groups_item_id, **kwargs)
        if action == "put_admin_groups_item_id":
            return await run_blocking(client.put_admin_groups_item_id, **kwargs)
        if action == "delete_admin_groups_item_id":
            return await run_blocking(client.delete_admin_groups_item_id, **kwargs)
        if action == "check_email_config":
            return await run_blocking(client.check_email_config, **kwargs)
        if action == "send_test_email":
            return await run_blocking(client.send_test_email, **kwargs)
        if action == "get_admin_backups":
            return await run_blocking(client.get_admin_backups, **kwargs)
        if action == "post_admin_backups":
            return await run_blocking(client.post_admin_backups, **kwargs)
        if action == "get_admin_backups_file_name":
            return await run_blocking(client.get_admin_backups_file_name, **kwargs)
        if action == "delete_admin_backups_file_name":
            return await run_blocking(client.delete_admin_backups_file_name, **kwargs)
        if action == "upload_one":
            return await run_blocking(client.upload_one, **kwargs)
        if action == "import_one":
            return await run_blocking(client.import_one, **kwargs)
        if action == "get_maintenance_summary":
            return await run_blocking(client.get_maintenance_summary, **kwargs)
        if action == "get_storage_details":
            return await run_blocking(client.get_storage_details, **kwargs)
        if action == "clean_images":
            return await run_blocking(client.clean_images, **kwargs)
        if action == "clean_temp":
            return await run_blocking(client.clean_temp, **kwargs)
        if action == "clean_recipe_folders":
            return await run_blocking(client.clean_recipe_folders, **kwargs)
        if action == "debug_openai":
            return await run_blocking(client.debug_openai, **kwargs)
        raise ValueError(f"Unknown action: {action}")


VALID_EXPLORE_ACTIONS = (
    "get_explore_groups_group_slug_foods",
    "get_explore_groups_group_slug_foods_item_id",
    "get_explore_groups_group_slug_households",
    "get_household",
    "get_explore_groups_group_slug_organizers_categories",
    "get_explore_groups_group_slug_organizers_categories_item_id",
    "get_explore_groups_group_slug_organizers_tags",
    "get_explore_groups_group_slug_organizers_tags_item_id",
    "get_explore_groups_group_slug_organizerss",
    "get_explore_groups_group_slug_organizerss_item_id",
    "get_explore_groups_group_slug_cookbooks",
    "get_explore_groups_group_slug_cookbooks_item_id",
    "get_explore_groups_group_slug_recipes",
    "get_explore_groups_group_slug_recipes_suggestions",
    "get_recipe",
)


def register_explore_tools(mcp: FastMCP):
    @mcp.tool(tags={"explore"})
    async def mealie_explore(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_explore_groups_group_slug_foods', 'get_explore_groups_group_slug_foods_item_id', 'get_explore_groups_group_slug_households', 'get_household', 'get_explore_groups_group_slug_organizers_categories', 'get_explore_groups_group_slug_organizers_categories_item_id', 'get_explore_groups_group_slug_organizers_tags', 'get_explore_groups_group_slug_organizers_tags_item_id', 'get_explore_groups_group_slug_organizerss', 'get_explore_groups_group_slug_organizerss_item_id', 'get_explore_groups_group_slug_cookbooks', 'get_explore_groups_group_slug_cookbooks_item_id', 'get_explore_groups_group_slug_recipes', 'get_explore_groups_group_slug_recipes_suggestions', 'get_recipe'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage mealie explore operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, VALID_EXPLORE_ACTIONS, service="mealie-mcp")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_explore_groups_group_slug_foods":
            return await run_blocking(
                client.get_explore_groups_group_slug_foods, **kwargs
            )
        if action == "get_explore_groups_group_slug_foods_item_id":
            return await run_blocking(
                client.get_explore_groups_group_slug_foods_item_id, **kwargs
            )
        if action == "get_explore_groups_group_slug_households":
            return await run_blocking(
                client.get_explore_groups_group_slug_households, **kwargs
            )
        if action == "get_household":
            return await run_blocking(client.get_household, **kwargs)
        if action == "get_explore_groups_group_slug_organizers_categories":
            return await run_blocking(
                client.get_explore_groups_group_slug_organizers_categories, **kwargs
            )
        if action == "get_explore_groups_group_slug_organizers_categories_item_id":
            return await run_blocking(
                client.get_explore_groups_group_slug_organizers_categories_item_id,
                **kwargs,
            )
        if action == "get_explore_groups_group_slug_organizers_tags":
            return await run_blocking(
                client.get_explore_groups_group_slug_organizers_tags, **kwargs
            )
        if action == "get_explore_groups_group_slug_organizers_tags_item_id":
            return await run_blocking(
                client.get_explore_groups_group_slug_organizers_tags_item_id, **kwargs
            )
        if action == "get_explore_groups_group_slug_organizerss":
            return await run_blocking(
                client.get_explore_groups_group_slug_organizerss, **kwargs
            )
        if action == "get_explore_groups_group_slug_organizerss_item_id":
            return await run_blocking(
                client.get_explore_groups_group_slug_organizerss_item_id, **kwargs
            )
        if action == "get_explore_groups_group_slug_cookbooks":
            return await run_blocking(
                client.get_explore_groups_group_slug_cookbooks, **kwargs
            )
        if action == "get_explore_groups_group_slug_cookbooks_item_id":
            return await run_blocking(
                client.get_explore_groups_group_slug_cookbooks_item_id, **kwargs
            )
        if action == "get_explore_groups_group_slug_recipes":
            return await run_blocking(
                client.get_explore_groups_group_slug_recipes, **kwargs
            )
        if action == "get_explore_groups_group_slug_recipes_suggestions":
            return await run_blocking(
                client.get_explore_groups_group_slug_recipes_suggestions, **kwargs
            )
        if action == "get_recipe":
            return await run_blocking(client.get_recipe, **kwargs)
        raise ValueError(f"Unknown action: {action}")


VALID_UTILS_ACTIONS = ("download_file",)


def register_utils_tools(mcp: FastMCP):
    @mcp.tool(tags={"utils"})
    async def mealie_utils(
        action: str = Field(
            description="Action to perform. Must be one of: 'download_file'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage mealie utils operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, VALID_UTILS_ACTIONS, service="mealie-mcp")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "download_file":
            return await run_blocking(client.download_file, **kwargs)
        raise ValueError(f"Unknown action: {action}")


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance."""
    load_config()
    args, mcp, middlewares = create_mcp_server(
        name="mealie-mcp MCP",
        version=__version__,
        instructions="mealie-mcp MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    DEFAULT_APPTOOL = to_boolean(os.getenv("APPTOOL", "True"))
    if DEFAULT_APPTOOL:
        register_app_tools(mcp)
    DEFAULT_USERSTOOL = to_boolean(os.getenv("USERSTOOL", "True"))
    if DEFAULT_USERSTOOL:
        register_users_tools(mcp)
    DEFAULT_HOUSEHOLDSTOOL = to_boolean(os.getenv("HOUSEHOLDSTOOL", "True"))
    if DEFAULT_HOUSEHOLDSTOOL:
        register_households_tools(mcp)
    DEFAULT_GROUPSTOOL = to_boolean(os.getenv("GROUPSTOOL", "True"))
    if DEFAULT_GROUPSTOOL:
        register_groups_tools(mcp)
    DEFAULT_RECIPESTOOL = to_boolean(os.getenv("RECIPESTOOL", "True"))
    if DEFAULT_RECIPESTOOL:
        register_recipes_tools(mcp)
    DEFAULT_ORGANIZERTOOL = to_boolean(os.getenv("ORGANIZERTOOL", "True"))
    if DEFAULT_ORGANIZERTOOL:
        register_organizer_tools(mcp)
    DEFAULT_SHAREDTOOL = to_boolean(os.getenv("SHAREDTOOL", "True"))
    if DEFAULT_SHAREDTOOL:
        register_shared_tools(mcp)
    DEFAULT_ADMINTOOL = to_boolean(os.getenv("ADMINTOOL", "True"))
    if DEFAULT_ADMINTOOL:
        register_admin_tools(mcp)
    DEFAULT_EXPLORETOOL = to_boolean(os.getenv("EXPLORETOOL", "True"))
    if DEFAULT_EXPLORETOOL:
        register_explore_tools(mcp)
    DEFAULT_UTILSTOOL = to_boolean(os.getenv("UTILSTOOL", "True"))
    if DEFAULT_UTILSTOOL:
        register_utils_tools(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
    mcp, args, middlewares = get_mcp_instance()
    print(f"mealie-mcp MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
