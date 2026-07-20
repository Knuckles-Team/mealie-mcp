"""MCP tools for users operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
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
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
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
