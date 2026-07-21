"""MCP tools for organizer operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from mealie_mcp.auth import get_client

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
