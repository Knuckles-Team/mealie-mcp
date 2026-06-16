"""MCP tools for users operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp_utilities import resolve_action
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
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, VALID_USERS_ACTIONS, service="mealie-mcp")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_token":
            return client.get_token(**kwargs)
        if action == "oauth_login":
            return client.oauth_login(**kwargs)
        if action == "oauth_callback":
            return client.oauth_callback(**kwargs)
        if action == "refresh_token":
            return client.refresh_token(**kwargs)
        if action == "logout":
            return client.logout(**kwargs)
        if action == "register_new_user":
            return client.register_new_user(**kwargs)
        if action == "get_logged_in_user":
            return client.get_logged_in_user(**kwargs)
        if action == "get_logged_in_user_ratings":
            return client.get_logged_in_user_ratings(**kwargs)
        if action == "get_logged_in_user_rating_for_recipe":
            return client.get_logged_in_user_rating_for_recipe(**kwargs)
        if action == "get_logged_in_user_favorites":
            return client.get_logged_in_user_favorites(**kwargs)
        if action == "update_password":
            return client.update_password(**kwargs)
        if action == "update_user":
            return client.update_user(**kwargs)
        if action == "forgot_password":
            return client.forgot_password(**kwargs)
        if action == "reset_password":
            return client.reset_password(**kwargs)
        if action == "update_user_image":
            return client.update_user_image(**kwargs)
        if action == "create":
            return client.create(**kwargs)
        if action == "delete":
            return client.delete(**kwargs)
        if action == "get_ratings":
            return client.get_ratings(**kwargs)
        if action == "get_favorites":
            return client.get_favorites(**kwargs)
        if action == "set_rating":
            return client.set_rating(**kwargs)
        if action == "add_favorite":
            return client.add_favorite(**kwargs)
        if action == "remove_favorite":
            return client.remove_favorite(**kwargs)
        raise ValueError(f"Unknown action: {action}")
