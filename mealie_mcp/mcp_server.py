#!/usr/bin/python
import warnings

from agent_utilities.core.config import load_config
from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
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
import sys
from typing import Any

from agent_utilities.mcp.server_factory import create_mcp_server
from agent_utilities.mcp.verbose_tools import register_tool_surface
from starlette.requests import Request
from starlette.responses import JSONResponse

from mealie_mcp.api_client import Api
from mealie_mcp.auth import get_client
from mealie_mcp.recipe_tools import (
    add_recipe_write_tools as _add_recipe_write_tools,
)

__version__ = "2.1.0"

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
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

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
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

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


async def _households_get_households_cookbooks(client, **kwargs):
    return await run_blocking(client.get_households_cookbooks, **kwargs)


async def _households_post_households_cookbooks(client, **kwargs):
    return await run_blocking(client.post_households_cookbooks, **kwargs)


async def _households_put_households_cookbooks(client, **kwargs):
    return await run_blocking(client.put_households_cookbooks, **kwargs)


async def _households_get_households_cookbooks_item_id(client, **kwargs):
    return await run_blocking(client.get_households_cookbooks_item_id, **kwargs)


async def _households_put_households_cookbooks_item_id(client, **kwargs):
    return await run_blocking(client.put_households_cookbooks_item_id, **kwargs)


async def _households_delete_households_cookbooks_item_id(client, **kwargs):
    return await run_blocking(client.delete_households_cookbooks_item_id, **kwargs)


async def _households_get_households_events_notifications(client, **kwargs):
    return await run_blocking(client.get_households_events_notifications, **kwargs)


async def _households_post_households_events_notifications(client, **kwargs):
    return await run_blocking(client.post_households_events_notifications, **kwargs)


async def _households_get_households_events_notifications_item_id(client, **kwargs):
    return await run_blocking(
        client.get_households_events_notifications_item_id, **kwargs
    )


async def _households_put_households_events_notifications_item_id(client, **kwargs):
    return await run_blocking(
        client.put_households_events_notifications_item_id, **kwargs
    )


async def _households_delete_households_events_notifications_item_id(client, **kwargs):
    return await run_blocking(
        client.delete_households_events_notifications_item_id, **kwargs
    )


async def _households_test_notification(client, **kwargs):
    return await run_blocking(client.test_notification, **kwargs)


async def _households_get_households_recipe_actions(client, **kwargs):
    return await run_blocking(client.get_households_recipe_actions, **kwargs)


async def _households_post_households_recipe_actions(client, **kwargs):
    return await run_blocking(client.post_households_recipe_actions, **kwargs)


async def _households_get_households_recipe_actions_item_id(client, **kwargs):
    return await run_blocking(client.get_households_recipe_actions_item_id, **kwargs)


async def _households_put_households_recipe_actions_item_id(client, **kwargs):
    return await run_blocking(client.put_households_recipe_actions_item_id, **kwargs)


async def _households_delete_households_recipe_actions_item_id(client, **kwargs):
    return await run_blocking(client.delete_households_recipe_actions_item_id, **kwargs)


async def _households_trigger_action(client, **kwargs):
    return await run_blocking(client.trigger_action, **kwargs)


async def _households_get_logged_in_user_household(client, **kwargs):
    return await run_blocking(client.get_logged_in_user_household, **kwargs)


async def _households_get_household_recipe(client, **kwargs):
    return await run_blocking(client.get_household_recipe, **kwargs)


async def _households_get_household_members(client, **kwargs):
    return await run_blocking(client.get_household_members, **kwargs)


async def _households_get_household_preferences(client, **kwargs):
    return await run_blocking(client.get_household_preferences, **kwargs)


async def _households_update_household_preferences(client, **kwargs):
    return await run_blocking(client.update_household_preferences, **kwargs)


async def _households_set_member_permissions(client, **kwargs):
    return await run_blocking(client.set_member_permissions, **kwargs)


async def _households_get_statistics(client, **kwargs):
    return await run_blocking(client.get_statistics, **kwargs)


async def _households_get_invite_tokens(client, **kwargs):
    return await run_blocking(client.get_invite_tokens, **kwargs)


async def _households_create_invite_token(client, **kwargs):
    return await run_blocking(client.create_invite_token, **kwargs)


async def _households_email_invitation(client, **kwargs):
    return await run_blocking(client.email_invitation, **kwargs)


async def _households_get_households_shopping_lists(client, **kwargs):
    return await run_blocking(client.get_households_shopping_lists, **kwargs)


async def _households_post_households_shopping_lists(client, **kwargs):
    return await run_blocking(client.post_households_shopping_lists, **kwargs)


async def _households_get_households_shopping_lists_item_id(client, **kwargs):
    return await run_blocking(client.get_households_shopping_lists_item_id, **kwargs)


async def _households_put_households_shopping_lists_item_id(client, **kwargs):
    return await run_blocking(client.put_households_shopping_lists_item_id, **kwargs)


async def _households_delete_households_shopping_lists_item_id(client, **kwargs):
    return await run_blocking(client.delete_households_shopping_lists_item_id, **kwargs)


async def _households_update_label_settings(client, **kwargs):
    return await run_blocking(client.update_label_settings, **kwargs)


async def _households_add_recipe_ingredients_to_list(client, **kwargs):
    return await run_blocking(client.add_recipe_ingredients_to_list, **kwargs)


async def _households_add_single_recipe_ingredients_to_list(client, **kwargs):
    return await run_blocking(client.add_single_recipe_ingredients_to_list, **kwargs)


async def _households_remove_recipe_ingredients_from_list(client, **kwargs):
    return await run_blocking(client.remove_recipe_ingredients_from_list, **kwargs)


async def _households_get_households_shopping_items(client, **kwargs):
    return await run_blocking(client.get_households_shopping_items, **kwargs)


async def _households_post_households_shopping_items(client, **kwargs):
    return await run_blocking(client.post_households_shopping_items, **kwargs)


async def _households_put_households_shopping_items(client, **kwargs):
    return await run_blocking(client.put_households_shopping_items, **kwargs)


async def _households_delete_households_shopping_items(client, **kwargs):
    return await run_blocking(client.delete_households_shopping_items, **kwargs)


async def _households_post_households_shopping_items_create_bulk(client, **kwargs):
    return await run_blocking(
        client.post_households_shopping_items_create_bulk, **kwargs
    )


async def _households_get_households_shopping_items_item_id(client, **kwargs):
    return await run_blocking(client.get_households_shopping_items_item_id, **kwargs)


async def _households_put_households_shopping_items_item_id(client, **kwargs):
    return await run_blocking(client.put_households_shopping_items_item_id, **kwargs)


async def _households_delete_households_shopping_items_item_id(client, **kwargs):
    return await run_blocking(client.delete_households_shopping_items_item_id, **kwargs)


async def _households_get_households_webhooks(client, **kwargs):
    return await run_blocking(client.get_households_webhooks, **kwargs)


async def _households_post_households_webhooks(client, **kwargs):
    return await run_blocking(client.post_households_webhooks, **kwargs)


async def _households_rerun_webhooks(client, **kwargs):
    return await run_blocking(client.rerun_webhooks, **kwargs)


async def _households_get_households_webhooks_item_id(client, **kwargs):
    return await run_blocking(client.get_households_webhooks_item_id, **kwargs)


async def _households_put_households_webhooks_item_id(client, **kwargs):
    return await run_blocking(client.put_households_webhooks_item_id, **kwargs)


async def _households_delete_households_webhooks_item_id(client, **kwargs):
    return await run_blocking(client.delete_households_webhooks_item_id, **kwargs)


async def _households_test_one(client, **kwargs):
    return await run_blocking(client.test_one, **kwargs)


async def _households_get_households_mealplans_rules(client, **kwargs):
    return await run_blocking(client.get_households_mealplans_rules, **kwargs)


async def _households_post_households_mealplans_rules(client, **kwargs):
    return await run_blocking(client.post_households_mealplans_rules, **kwargs)


async def _households_get_households_mealplans_rules_item_id(client, **kwargs):
    return await run_blocking(client.get_households_mealplans_rules_item_id, **kwargs)


async def _households_put_households_mealplans_rules_item_id(client, **kwargs):
    return await run_blocking(client.put_households_mealplans_rules_item_id, **kwargs)


async def _households_delete_households_mealplans_rules_item_id(client, **kwargs):
    return await run_blocking(
        client.delete_households_mealplans_rules_item_id, **kwargs
    )


async def _households_get_households_mealplans(client, **kwargs):
    return await run_blocking(client.get_households_mealplans, **kwargs)


async def _households_post_households_mealplans(client, **kwargs):
    return await run_blocking(client.post_households_mealplans, **kwargs)


async def _households_get_todays_meals(client, **kwargs):
    return await run_blocking(client.get_todays_meals, **kwargs)


async def _households_create_random_meal(client, **kwargs):
    return await run_blocking(client.create_random_meal, **kwargs)


async def _households_get_households_mealplans_item_id(client, **kwargs):
    return await run_blocking(client.get_households_mealplans_item_id, **kwargs)


async def _households_put_households_mealplans_item_id(client, **kwargs):
    return await run_blocking(client.put_households_mealplans_item_id, **kwargs)


async def _households_delete_households_mealplans_item_id(client, **kwargs):
    return await run_blocking(client.delete_households_mealplans_item_id, **kwargs)


_HOUSEHOLDS_ACTION_HANDLERS = {
    "get_households_cookbooks": _households_get_households_cookbooks,
    "post_households_cookbooks": _households_post_households_cookbooks,
    "put_households_cookbooks": _households_put_households_cookbooks,
    "get_households_cookbooks_item_id": _households_get_households_cookbooks_item_id,
    "put_households_cookbooks_item_id": _households_put_households_cookbooks_item_id,
    "delete_households_cookbooks_item_id": _households_delete_households_cookbooks_item_id,
    "get_households_events_notifications": _households_get_households_events_notifications,
    "post_households_events_notifications": _households_post_households_events_notifications,
    "get_households_events_notifications_item_id": _households_get_households_events_notifications_item_id,
    "put_households_events_notifications_item_id": _households_put_households_events_notifications_item_id,
    "delete_households_events_notifications_item_id": _households_delete_households_events_notifications_item_id,
    "test_notification": _households_test_notification,
    "get_households_recipe_actions": _households_get_households_recipe_actions,
    "post_households_recipe_actions": _households_post_households_recipe_actions,
    "get_households_recipe_actions_item_id": _households_get_households_recipe_actions_item_id,
    "put_households_recipe_actions_item_id": _households_put_households_recipe_actions_item_id,
    "delete_households_recipe_actions_item_id": _households_delete_households_recipe_actions_item_id,
    "trigger_action": _households_trigger_action,
    "get_logged_in_user_household": _households_get_logged_in_user_household,
    "get_household_recipe": _households_get_household_recipe,
    "get_household_members": _households_get_household_members,
    "get_household_preferences": _households_get_household_preferences,
    "update_household_preferences": _households_update_household_preferences,
    "set_member_permissions": _households_set_member_permissions,
    "get_statistics": _households_get_statistics,
    "get_invite_tokens": _households_get_invite_tokens,
    "create_invite_token": _households_create_invite_token,
    "email_invitation": _households_email_invitation,
    "get_households_shopping_lists": _households_get_households_shopping_lists,
    "post_households_shopping_lists": _households_post_households_shopping_lists,
    "get_households_shopping_lists_item_id": _households_get_households_shopping_lists_item_id,
    "put_households_shopping_lists_item_id": _households_put_households_shopping_lists_item_id,
    "delete_households_shopping_lists_item_id": _households_delete_households_shopping_lists_item_id,
    "update_label_settings": _households_update_label_settings,
    "add_recipe_ingredients_to_list": _households_add_recipe_ingredients_to_list,
    "add_single_recipe_ingredients_to_list": _households_add_single_recipe_ingredients_to_list,
    "remove_recipe_ingredients_from_list": _households_remove_recipe_ingredients_from_list,
    "get_households_shopping_items": _households_get_households_shopping_items,
    "post_households_shopping_items": _households_post_households_shopping_items,
    "put_households_shopping_items": _households_put_households_shopping_items,
    "delete_households_shopping_items": _households_delete_households_shopping_items,
    "post_households_shopping_items_create_bulk": _households_post_households_shopping_items_create_bulk,
    "get_households_shopping_items_item_id": _households_get_households_shopping_items_item_id,
    "put_households_shopping_items_item_id": _households_put_households_shopping_items_item_id,
    "delete_households_shopping_items_item_id": _households_delete_households_shopping_items_item_id,
    "get_households_webhooks": _households_get_households_webhooks,
    "post_households_webhooks": _households_post_households_webhooks,
    "rerun_webhooks": _households_rerun_webhooks,
    "get_households_webhooks_item_id": _households_get_households_webhooks_item_id,
    "put_households_webhooks_item_id": _households_put_households_webhooks_item_id,
    "delete_households_webhooks_item_id": _households_delete_households_webhooks_item_id,
    "test_one": _households_test_one,
    "get_households_mealplans_rules": _households_get_households_mealplans_rules,
    "post_households_mealplans_rules": _households_post_households_mealplans_rules,
    "get_households_mealplans_rules_item_id": _households_get_households_mealplans_rules_item_id,
    "put_households_mealplans_rules_item_id": _households_put_households_mealplans_rules_item_id,
    "delete_households_mealplans_rules_item_id": _households_delete_households_mealplans_rules_item_id,
    "get_households_mealplans": _households_get_households_mealplans,
    "post_households_mealplans": _households_post_households_mealplans,
    "get_todays_meals": _households_get_todays_meals,
    "create_random_meal": _households_create_random_meal,
    "get_households_mealplans_item_id": _households_get_households_mealplans_item_id,
    "put_households_mealplans_item_id": _households_put_households_mealplans_item_id,
    "delete_households_mealplans_item_id": _households_delete_households_mealplans_item_id,
}


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
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, VALID_HOUSEHOLDS_ACTIONS, service="mealie-mcp"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        handler = _HOUSEHOLDS_ACTION_HANDLERS.get(action)
        if handler is None:
            raise ValueError(f"Unknown action: {action}")
        return await handler(client, **kwargs)


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
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

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


async def _recipes_get_recipe_formats_and_templates(client, **kwargs):
    return await run_blocking(client.get_recipe_formats_and_templates, **kwargs)


async def _recipes_get_recipe_as_format(client, **kwargs):
    return await run_blocking(client.get_recipe_as_format, **kwargs)


async def _recipes_test_parse_recipe_url(client, **kwargs):
    return await run_blocking(client.test_parse_recipe_url, **kwargs)


async def _recipes_create_recipe_from_html_or_json(client, **kwargs):
    return await run_blocking(client.create_recipe_from_html_or_json, **kwargs)


async def _recipes_parse_recipe_url(client, **kwargs):
    return await run_blocking(client.parse_recipe_url, **kwargs)


async def _recipes_parse_recipe_url_bulk(client, **kwargs):
    return await run_blocking(client.parse_recipe_url_bulk, **kwargs)


async def _recipes_create_recipe_from_zip(client, **kwargs):
    return await run_blocking(client.create_recipe_from_zip, **kwargs)


async def _recipes_create_recipe_from_image(client, **kwargs):
    return await run_blocking(client.create_recipe_from_image, **kwargs)


async def _recipes_get_recipes(client, **kwargs):
    return await run_blocking(client.get_recipes, **kwargs)


async def _recipes_post_recipes(client, **kwargs):
    return await run_blocking(client.post_recipes, **kwargs)


async def _recipes_put_recipes(client, **kwargs):
    return await run_blocking(client.put_recipes, **kwargs)


async def _recipes_patch_many(client, **kwargs):
    return await run_blocking(client.patch_many, **kwargs)


async def _recipes_get_recipes_suggestions(client, **kwargs):
    return await run_blocking(client.get_recipes_suggestions, **kwargs)


async def _recipes_get_recipes_slug(client, **kwargs):
    return await run_blocking(client.get_recipes_slug, **kwargs)


async def _recipes_put_recipes_slug(client, **kwargs):
    return await run_blocking(client.put_recipes_slug, **kwargs)


async def _recipes_patch_one(client, **kwargs):
    return await run_blocking(client.patch_one, **kwargs)


async def _recipes_delete_recipes_slug(client, **kwargs):
    return await run_blocking(client.delete_recipes_slug, **kwargs)


async def _recipes_duplicate_one(client, **kwargs):
    return await run_blocking(client.duplicate_one, **kwargs)


async def _recipes_update_last_made(client, **kwargs):
    return await run_blocking(client.update_last_made, **kwargs)


async def _recipes_scrape_image_url(client, **kwargs):
    return await run_blocking(client.scrape_image_url, **kwargs)


async def _recipes_update_recipe_image(client, **kwargs):
    return await run_blocking(client.update_recipe_image, **kwargs)


async def _recipes_delete_recipe_image(client, **kwargs):
    return await run_blocking(client.delete_recipe_image, **kwargs)


async def _recipes_upload_recipe_asset(client, **kwargs):
    return await run_blocking(client.upload_recipe_asset, **kwargs)


async def _recipes_get_recipe_comments(client, **kwargs):
    return await run_blocking(client.get_recipe_comments, **kwargs)


async def _recipes_bulk_tag_recipes(client, **kwargs):
    return await run_blocking(client.bulk_tag_recipes, **kwargs)


async def _recipes_bulk_settings_recipes(client, **kwargs):
    return await run_blocking(client.bulk_settings_recipes, **kwargs)


async def _recipes_bulk_categorize_recipes(client, **kwargs):
    return await run_blocking(client.bulk_categorize_recipes, **kwargs)


async def _recipes_bulk_delete_recipes(client, **kwargs):
    return await run_blocking(client.bulk_delete_recipes, **kwargs)


async def _recipes_bulk_export_recipes(client, **kwargs):
    return await run_blocking(client.bulk_export_recipes, **kwargs)


async def _recipes_get_exported_data(client, **kwargs):
    return await run_blocking(client.get_exported_data, **kwargs)


async def _recipes_get_exported_data_token(client, **kwargs):
    return await run_blocking(client.get_exported_data_token, **kwargs)


async def _recipes_purge_export_data(client, **kwargs):
    return await run_blocking(client.purge_export_data, **kwargs)


async def _recipes_get_shared_recipe(client, **kwargs):
    return await run_blocking(client.get_shared_recipe, **kwargs)


async def _recipes_get_shared_recipe_as_zip(client, **kwargs):
    return await run_blocking(client.get_shared_recipe_as_zip, **kwargs)


async def _recipes_get_recipes_timeline_events(client, **kwargs):
    return await run_blocking(client.get_recipes_timeline_events, **kwargs)


async def _recipes_post_recipes_timeline_events(client, **kwargs):
    return await run_blocking(client.post_recipes_timeline_events, **kwargs)


async def _recipes_get_recipes_timeline_events_item_id(client, **kwargs):
    return await run_blocking(client.get_recipes_timeline_events_item_id, **kwargs)


async def _recipes_put_recipes_timeline_events_item_id(client, **kwargs):
    return await run_blocking(client.put_recipes_timeline_events_item_id, **kwargs)


async def _recipes_delete_recipes_timeline_events_item_id(client, **kwargs):
    return await run_blocking(client.delete_recipes_timeline_events_item_id, **kwargs)


async def _recipes_update_event_image(client, **kwargs):
    return await run_blocking(client.update_event_image, **kwargs)


async def _recipes_get_comments(client, **kwargs):
    return await run_blocking(client.get_comments, **kwargs)


async def _recipes_post_comments(client, **kwargs):
    return await run_blocking(client.post_comments, **kwargs)


async def _recipes_get_comments_item_id(client, **kwargs):
    return await run_blocking(client.get_comments_item_id, **kwargs)


async def _recipes_put_comments_item_id(client, **kwargs):
    return await run_blocking(client.put_comments_item_id, **kwargs)


async def _recipes_post_parser_ingredient(client, **kwargs):
    return await run_blocking(client.post_parser_ingredient, **kwargs)


async def _recipes_parse_ingredient(client, **kwargs):
    return await run_blocking(client.parse_ingredient, **kwargs)


async def _recipes_parse_ingredients(client, **kwargs):
    return await run_blocking(client.parse_ingredients, **kwargs)


async def _recipes_get_foods(client, **kwargs):
    return await run_blocking(client.get_foods, **kwargs)


async def _recipes_post_foods(client, **kwargs):
    return await run_blocking(client.post_foods, **kwargs)


async def _recipes_put_foods_merge(client, **kwargs):
    return await run_blocking(client.put_foods_merge, **kwargs)


async def _recipes_get_foods_item_id(client, **kwargs):
    return await run_blocking(client.get_foods_item_id, **kwargs)


async def _recipes_put_foods_item_id(client, **kwargs):
    return await run_blocking(client.put_foods_item_id, **kwargs)


async def _recipes_delete_foods_item_id(client, **kwargs):
    return await run_blocking(client.delete_foods_item_id, **kwargs)


async def _recipes_get_units(client, **kwargs):
    return await run_blocking(client.get_units, **kwargs)


async def _recipes_post_units(client, **kwargs):
    return await run_blocking(client.post_units, **kwargs)


async def _recipes_put_units_merge(client, **kwargs):
    return await run_blocking(client.put_units_merge, **kwargs)


async def _recipes_get_units_item_id(client, **kwargs):
    return await run_blocking(client.get_units_item_id, **kwargs)


async def _recipes_put_units_item_id(client, **kwargs):
    return await run_blocking(client.put_units_item_id, **kwargs)


async def _recipes_delete_units_item_id(client, **kwargs):
    return await run_blocking(client.delete_units_item_id, **kwargs)


async def _recipes_get_recipe_img(client, **kwargs):
    return await run_blocking(client.get_recipe_img, **kwargs)


async def _recipes_get_recipe_timeline_event_img(client, **kwargs):
    return await run_blocking(client.get_recipe_timeline_event_img, **kwargs)


async def _recipes_get_recipe_asset(client, **kwargs):
    return await run_blocking(client.get_recipe_asset, **kwargs)


async def _recipes_get_user_image(client, **kwargs):
    return await run_blocking(client.get_user_image, **kwargs)


async def _recipes_get_validation_text(client, **kwargs):
    return await run_blocking(client.get_validation_text, **kwargs)


_RECIPES_ACTION_HANDLERS = {
    "get_recipe_formats_and_templates": _recipes_get_recipe_formats_and_templates,
    "get_recipe_as_format": _recipes_get_recipe_as_format,
    "test_parse_recipe_url": _recipes_test_parse_recipe_url,
    "create_recipe_from_html_or_json": _recipes_create_recipe_from_html_or_json,
    "parse_recipe_url": _recipes_parse_recipe_url,
    "parse_recipe_url_bulk": _recipes_parse_recipe_url_bulk,
    "create_recipe_from_zip": _recipes_create_recipe_from_zip,
    "create_recipe_from_image": _recipes_create_recipe_from_image,
    "get_recipes": _recipes_get_recipes,
    "post_recipes": _recipes_post_recipes,
    "put_recipes": _recipes_put_recipes,
    "patch_many": _recipes_patch_many,
    "get_recipes_suggestions": _recipes_get_recipes_suggestions,
    "get_recipes_slug": _recipes_get_recipes_slug,
    "put_recipes_slug": _recipes_put_recipes_slug,
    "patch_one": _recipes_patch_one,
    "delete_recipes_slug": _recipes_delete_recipes_slug,
    "duplicate_one": _recipes_duplicate_one,
    "update_last_made": _recipes_update_last_made,
    "scrape_image_url": _recipes_scrape_image_url,
    "update_recipe_image": _recipes_update_recipe_image,
    "delete_recipe_image": _recipes_delete_recipe_image,
    "upload_recipe_asset": _recipes_upload_recipe_asset,
    "get_recipe_comments": _recipes_get_recipe_comments,
    "bulk_tag_recipes": _recipes_bulk_tag_recipes,
    "bulk_settings_recipes": _recipes_bulk_settings_recipes,
    "bulk_categorize_recipes": _recipes_bulk_categorize_recipes,
    "bulk_delete_recipes": _recipes_bulk_delete_recipes,
    "bulk_export_recipes": _recipes_bulk_export_recipes,
    "get_exported_data": _recipes_get_exported_data,
    "get_exported_data_token": _recipes_get_exported_data_token,
    "purge_export_data": _recipes_purge_export_data,
    "get_shared_recipe": _recipes_get_shared_recipe,
    "get_shared_recipe_as_zip": _recipes_get_shared_recipe_as_zip,
    "get_recipes_timeline_events": _recipes_get_recipes_timeline_events,
    "post_recipes_timeline_events": _recipes_post_recipes_timeline_events,
    "get_recipes_timeline_events_item_id": _recipes_get_recipes_timeline_events_item_id,
    "put_recipes_timeline_events_item_id": _recipes_put_recipes_timeline_events_item_id,
    "delete_recipes_timeline_events_item_id": _recipes_delete_recipes_timeline_events_item_id,
    "update_event_image": _recipes_update_event_image,
    "get_comments": _recipes_get_comments,
    "post_comments": _recipes_post_comments,
    "get_comments_item_id": _recipes_get_comments_item_id,
    "put_comments_item_id": _recipes_put_comments_item_id,
    "post_parser_ingredient": _recipes_post_parser_ingredient,
    "parse_ingredient": _recipes_parse_ingredient,
    "parse_ingredients": _recipes_parse_ingredients,
    "get_foods": _recipes_get_foods,
    "post_foods": _recipes_post_foods,
    "put_foods_merge": _recipes_put_foods_merge,
    "get_foods_item_id": _recipes_get_foods_item_id,
    "put_foods_item_id": _recipes_put_foods_item_id,
    "delete_foods_item_id": _recipes_delete_foods_item_id,
    "get_units": _recipes_get_units,
    "post_units": _recipes_post_units,
    "put_units_merge": _recipes_put_units_merge,
    "get_units_item_id": _recipes_get_units_item_id,
    "put_units_item_id": _recipes_put_units_item_id,
    "delete_units_item_id": _recipes_delete_units_item_id,
    "get_recipe_img": _recipes_get_recipe_img,
    "get_recipe_timeline_event_img": _recipes_get_recipe_timeline_event_img,
    "get_recipe_asset": _recipes_get_recipe_asset,
    "get_user_image": _recipes_get_user_image,
    "get_validation_text": _recipes_get_validation_text,
}


def register_recipes_tools(mcp: FastMCP):
    _add_recipe_write_tools(mcp)

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
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, VALID_RECIPES_ACTIONS, service="mealie-mcp")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        handler = _RECIPES_ACTION_HANDLERS.get(action)
        if handler is None:
            raise ValueError(f"Unknown action: {action}")
        return await handler(client, **kwargs)


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
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

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
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

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
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

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
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

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
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, VALID_UTILS_ACTIONS, service="mealie-mcp")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "download_file":
            return await run_blocking(client.download_file, **kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_kg_tools(mcp: FastMCP):
    @mcp.tool(tags={"kg"})
    async def mealie_ingest_recipes(
        params_json: str = Field(
            default="{}",
            description='JSON string of get_recipes filters (e.g. {"per_page": 100, "categories": "Dinner"}).',
        ),
        ingest_images: bool = Field(
            default=False,
            description="Also fetch each recipe image and store it as a :AssetOccurrence blob.",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Natively ingest Mealie recipes into epistemic-graph as typed :Recipe nodes.

        Lists recipes via the Mealie API and pushes them (with their :Ingredient,
        :Food, :Unit, :RecipeCategory, :Tag and :RecipeTool nodes + links) into the
        knowledge graph via the fast engine client. With ``ingest_images`` the raw
        image bytes are stored as content-addressed :AssetOccurrence blobs. Best-effort:
        returns ``{"ingested": None}`` when no engine is reachable.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        import json as _json

        from mealie_mcp.kg_ingest import ingest_recipes
        from mealie_mcp.kg_media import fetch_recipe_image_bytes, ingest_recipe_image

        if ctx:
            await ctx.info("Listing recipes for KG ingestion...")
        try:
            kwargs = _json.loads(params_json) if params_json else {}
        except Exception:  # noqa: BLE001
            return {"error": "Operation failed"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resp = await run_blocking(client.get_recipes, **kwargs)
        data = resp.get("items", resp) if isinstance(resp, dict) else resp
        records = data if isinstance(data, list) else [data]
        recipes = [r for r in records if isinstance(r, dict) and r.get("id")]

        result = ingest_recipes(recipes)

        images = 0
        if ingest_images:
            for recipe in recipes:
                image_bytes = await run_blocking(
                    fetch_recipe_image_bytes, client, str(recipe["id"])
                )
                if not image_bytes:
                    continue
                if ingest_recipe_image(recipe, image_bytes=image_bytes) is not None:
                    images += 1

        return {"listed": len(recipes), "ingested": result, "images_ingested": images}

    return None


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

    register_tool_surface(
        mcp,
        client_cls=Api,
        get_client=get_client,
        service="mealie-mcp",
        tools_module=sys.modules[__name__],
    )

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
