"""MCP tools for admin operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from mealie_mcp.auth import get_client

VALID_ADMIN_ACTIONS = (
    "get_app_info",
    "get_app_statistics",
    "check_app_config",
    "get_admin_users",
    "post_admin_users",
    "unlock_users",
    "get_admin_users_item_id",
    "put_admin_users_item_id",
    "delete_admin_users_item_id",
    "generate_token",
    "get_admin_households",
    "post_admin_households",
    "get_admin_households_item_id",
    "put_admin_households_item_id",
    "delete_admin_households_item_id",
    "get_admin_groups",
    "post_admin_groups",
    "get_admin_groups_item_id",
    "put_admin_groups_item_id",
    "delete_admin_groups_item_id",
    "check_email_config",
    "send_test_email",
    "get_admin_backups",
    "post_admin_backups",
    "get_admin_backups_file_name",
    "delete_admin_backups_file_name",
    "upload_one",
    "import_one",
    "get_maintenance_summary",
    "get_storage_details",
    "clean_images",
    "clean_temp",
    "clean_recipe_folders",
    "debug_openai",
)


def register_admin_tools(mcp: FastMCP):
    @mcp.tool(tags={"admin"})
    async def mealie_admin(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_app_info', 'get_app_statistics', 'check_app_config', 'get_admin_users', 'post_admin_users', 'unlock_users', 'get_admin_users_item_id', 'put_admin_users_item_id', 'delete_admin_users_item_id', 'generate_token', 'get_admin_households', 'post_admin_households', 'get_admin_households_item_id', 'put_admin_households_item_id', 'delete_admin_households_item_id', 'get_admin_groups', 'post_admin_groups', 'get_admin_groups_item_id', 'put_admin_groups_item_id', 'delete_admin_groups_item_id', 'check_email_config', 'send_test_email', 'get_admin_backups', 'post_admin_backups', 'get_admin_backups_file_name', 'delete_admin_backups_file_name', 'upload_one', 'import_one', 'get_maintenance_summary', 'get_storage_details', 'clean_images', 'clean_temp', 'clean_recipe_folders', 'debug_openai'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage mealie admin operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, VALID_ADMIN_ACTIONS, service="mealie-mcp")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_app_info":
            return await run_blocking(client.get_app_info, **kwargs)
        if action == "get_app_statistics":
            return await run_blocking(client.get_app_statistics, **kwargs)
        if action == "check_app_config":
            return await run_blocking(client.check_app_config, **kwargs)
        if action == "get_admin_users":
            return await run_blocking(client.get_admin_users, **kwargs)
        if action == "post_admin_users":
            return await run_blocking(client.post_admin_users, **kwargs)
        if action == "unlock_users":
            return await run_blocking(client.unlock_users, **kwargs)
        if action == "get_admin_users_item_id":
            return await run_blocking(client.get_admin_users_item_id, **kwargs)
        if action == "put_admin_users_item_id":
            return await run_blocking(client.put_admin_users_item_id, **kwargs)
        if action == "delete_admin_users_item_id":
            return await run_blocking(client.delete_admin_users_item_id, **kwargs)
        if action == "generate_token":
            return await run_blocking(client.generate_token, **kwargs)
        if action == "get_admin_households":
            return await run_blocking(client.get_admin_households, **kwargs)
        if action == "post_admin_households":
            return await run_blocking(client.post_admin_households, **kwargs)
        if action == "get_admin_households_item_id":
            return await run_blocking(client.get_admin_households_item_id, **kwargs)
        if action == "put_admin_households_item_id":
            return await run_blocking(client.put_admin_households_item_id, **kwargs)
        if action == "delete_admin_households_item_id":
            return await run_blocking(client.delete_admin_households_item_id, **kwargs)
        if action == "get_admin_groups":
            return await run_blocking(client.get_admin_groups, **kwargs)
        if action == "post_admin_groups":
            return await run_blocking(client.post_admin_groups, **kwargs)
        if action == "get_admin_groups_item_id":
            return await run_blocking(client.get_admin_groups_item_id, **kwargs)
        if action == "put_admin_groups_item_id":
            return await run_blocking(client.put_admin_groups_item_id, **kwargs)
        if action == "delete_admin_groups_item_id":
            return await run_blocking(client.delete_admin_groups_item_id, **kwargs)
        if action == "check_email_config":
            return await run_blocking(client.check_email_config, **kwargs)
        if action == "send_test_email":
            return await run_blocking(client.send_test_email, **kwargs)
        if action == "get_admin_backups":
            return await run_blocking(client.get_admin_backups, **kwargs)
        if action == "post_admin_backups":
            return await run_blocking(client.post_admin_backups, **kwargs)
        if action == "get_admin_backups_file_name":
            return await run_blocking(client.get_admin_backups_file_name, **kwargs)
        if action == "delete_admin_backups_file_name":
            return await run_blocking(client.delete_admin_backups_file_name, **kwargs)
        if action == "upload_one":
            return await run_blocking(client.upload_one, **kwargs)
        if action == "import_one":
            return await run_blocking(client.import_one, **kwargs)
        if action == "get_maintenance_summary":
            return await run_blocking(client.get_maintenance_summary, **kwargs)
        if action == "get_storage_details":
            return await run_blocking(client.get_storage_details, **kwargs)
        if action == "clean_images":
            return await run_blocking(client.clean_images, **kwargs)
        if action == "clean_temp":
            return await run_blocking(client.clean_temp, **kwargs)
        if action == "clean_recipe_folders":
            return await run_blocking(client.clean_recipe_folders, **kwargs)
        if action == "debug_openai":
            return await run_blocking(client.debug_openai, **kwargs)
        raise ValueError(f"Unknown action: {action}")
