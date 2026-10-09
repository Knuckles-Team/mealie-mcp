"""MCP tools for users operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_connector_sdk.mcp.action_dispatch import resolve_action
from agent_connector_sdk.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from mealie_mcp.auth import get_client

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

        return await run_blocking(getattr(client, action), **kwargs)
