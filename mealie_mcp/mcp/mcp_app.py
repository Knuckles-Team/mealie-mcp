"""MCP tools for app operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from mealie_mcp.auth import get_client


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
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_startup_info":
            return client.get_startup_info(**kwargs)
        if action == "get_app_theme":
            return client.get_app_theme(**kwargs)
        raise ValueError(f"Unknown action: {action}")
