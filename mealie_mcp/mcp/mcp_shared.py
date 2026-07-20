"""MCP tools for shared operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from mealie_mcp.auth import get_client

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
