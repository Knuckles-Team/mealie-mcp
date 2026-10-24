from agent_connector_sdk.connector import Connector

from mealie_mcp.api_client import Api
from mealie_mcp.auth import get_client

connector = Connector(
    api=Api,
    get_client=get_client,
    tools="mealie_mcp.mcp_server",
    instructions="mealie-mcp MCP Server — Condensed Action-Routed Tools.",
)
