"""MCP tools for groups operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp_utilities import resolve_action
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from mealie_mcp.auth import get_client

VALID_GROUPS_ACTIONS = (
    "get_all_households",
    "get_one_household",
    "get_logged_in_user_group",
    "get_group_members",
    "get_group_member",
    "get_group_preferences",
    "update_group_preferences",
    "get_storage",
    "start_data_migration",
    "get_groups_reports",
    "get_groups_reports_item_id",
    "delete_groups_reports_item_id",
    "get_groups_labels",
    "post_groups_labels",
    "get_groups_labels_item_id",
    "put_groups_labels_item_id",
    "delete_groups_labels_item_id",
    "seed_foods",
    "seed_labels",
    "seed_units",
)


def register_groups_tools(mcp: FastMCP):
    @mcp.tool(tags={"groups"})
    async def mealie_groups(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_all_households', 'get_one_household', 'get_logged_in_user_group', 'get_group_members', 'get_group_member', 'get_group_preferences', 'update_group_preferences', 'get_storage', 'start_data_migration', 'get_groups_reports', 'get_groups_reports_item_id', 'delete_groups_reports_item_id', 'get_groups_labels', 'post_groups_labels', 'get_groups_labels_item_id', 'put_groups_labels_item_id', 'delete_groups_labels_item_id', 'seed_foods', 'seed_labels', 'seed_units'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage mealie groups operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, VALID_GROUPS_ACTIONS, service="mealie-mcp")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_all_households":
            return client.get_all_households(**kwargs)
        if action == "get_one_household":
            return client.get_one_household(**kwargs)
        if action == "get_logged_in_user_group":
            return client.get_logged_in_user_group(**kwargs)
        if action == "get_group_members":
            return client.get_group_members(**kwargs)
        if action == "get_group_member":
            return client.get_group_member(**kwargs)
        if action == "get_group_preferences":
            return client.get_group_preferences(**kwargs)
        if action == "update_group_preferences":
            return client.update_group_preferences(**kwargs)
        if action == "get_storage":
            return client.get_storage(**kwargs)
        if action == "start_data_migration":
            return client.start_data_migration(**kwargs)
        if action == "get_groups_reports":
            return client.get_groups_reports(**kwargs)
        if action == "get_groups_reports_item_id":
            return client.get_groups_reports_item_id(**kwargs)
        if action == "delete_groups_reports_item_id":
            return client.delete_groups_reports_item_id(**kwargs)
        if action == "get_groups_labels":
            return client.get_groups_labels(**kwargs)
        if action == "post_groups_labels":
            return client.post_groups_labels(**kwargs)
        if action == "get_groups_labels_item_id":
            return client.get_groups_labels_item_id(**kwargs)
        if action == "put_groups_labels_item_id":
            return client.put_groups_labels_item_id(**kwargs)
        if action == "delete_groups_labels_item_id":
            return client.delete_groups_labels_item_id(**kwargs)
        if action == "seed_foods":
            return client.seed_foods(**kwargs)
        if action == "seed_labels":
            return client.seed_labels(**kwargs)
        if action == "seed_units":
            return client.seed_units(**kwargs)
        raise ValueError(f"Unknown action: {action}")
