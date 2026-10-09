"""MCP tools for households operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_connector_sdk.mcp.action_dispatch import resolve_action
from agent_connector_sdk.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from mealie_mcp.auth import get_client

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
