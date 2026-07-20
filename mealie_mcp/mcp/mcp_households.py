"""MCP tools for households operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
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
            return {"error": "Operation failed"}

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
