"""MCP tool registration modules for mealie-mcp.

Auto-generated during ecosystem standardization.
Each domain has its own module with a register_*_tools function.
"""

from mealie_mcp.mcp.mcp_admin import register_admin_tools
from mealie_mcp.mcp.mcp_app import register_app_tools
from mealie_mcp.mcp.mcp_explore import register_explore_tools
from mealie_mcp.mcp.mcp_groups import register_groups_tools
from mealie_mcp.mcp.mcp_households import register_households_tools
from mealie_mcp.mcp.mcp_organizer import register_organizer_tools
from mealie_mcp.mcp.mcp_recipes import register_recipes_tools
from mealie_mcp.mcp.mcp_shared import register_shared_tools
from mealie_mcp.mcp.mcp_users import register_users_tools
from mealie_mcp.mcp.mcp_utils import register_utils_tools

__all__ = [
    "register_admin_tools",
    "register_app_tools",
    "register_explore_tools",
    "register_groups_tools",
    "register_households_tools",
    "register_organizer_tools",
    "register_recipes_tools",
    "register_shared_tools",
    "register_users_tools",
    "register_utils_tools",
]
