"""MCP tools for explore operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from mealie_mcp.auth import get_client

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
