import sys
from unittest.mock import patch

from fastmcp import FastMCP

from scion_sdk.connector import build_server


def test_mcp_instance_creation():
    """Test that the MCP instance can be created successfully."""
    with patch.object(sys, "argv", [""]):
        _, mcp = build_server("mealie_mcp", command_args=[])
    assert isinstance(mcp, FastMCP)


def test_import_agent():
    """Test that the package can be imported."""
    pass
