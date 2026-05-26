"""MCP tools for organizer operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from mealie_mcp.auth import get_client


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

        if action == "get_organizers_categories":
            return client.get_organizers_categories(**kwargs)
        if action == "post_organizers_categories":
            return client.post_organizers_categories(**kwargs)
        if action == "get_all_empty":
            return client.get_all_empty(**kwargs)
        if action == "get_organizers_categories_item_id":
            return client.get_organizers_categories_item_id(**kwargs)
        if action == "put_organizers_categories_item_id":
            return client.put_organizers_categories_item_id(**kwargs)
        if action == "delete_organizers_categories_item_id":
            return client.delete_organizers_categories_item_id(**kwargs)
        if action == "get_organizers_categories_slug_category_slug":
            return client.get_organizers_categories_slug_category_slug(**kwargs)
        if action == "get_organizers_tags":
            return client.get_organizers_tags(**kwargs)
        if action == "post_organizers_tags":
            return client.post_organizers_tags(**kwargs)
        if action == "get_empty_tags":
            return client.get_empty_tags(**kwargs)
        if action == "get_organizers_tags_item_id":
            return client.get_organizers_tags_item_id(**kwargs)
        if action == "put_organizers_tags_item_id":
            return client.put_organizers_tags_item_id(**kwargs)
        if action == "delete_recipe_tag":
            return client.delete_recipe_tag(**kwargs)
        if action == "get_organizers_tags_slug_tag_slug":
            return client.get_organizers_tags_slug_tag_slug(**kwargs)
        if action == "get_organizerss":
            return client.get_organizerss(**kwargs)
        if action == "post_organizerss":
            return client.post_organizerss(**kwargs)
        if action == "get_organizerss_item_id":
            return client.get_organizerss_item_id(**kwargs)
        if action == "put_organizerss_item_id":
            return client.put_organizerss_item_id(**kwargs)
        if action == "delete_organizerss_item_id":
            return client.delete_organizerss_item_id(**kwargs)
        if action == "get_organizerss_slug_slug":
            return client.get_organizerss_slug_slug(**kwargs)
        raise ValueError(f"Unknown action: {action}")
