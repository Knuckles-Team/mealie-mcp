"""Authentication module for mealie-mcp."""

import os

from agent_utilities.base_utilities import get_logger, to_boolean

from mealie_mcp.api_client import Api

logger = get_logger(__name__)


def get_client():
    """Get authenticated client for mealie-mcp."""
    base_url = os.getenv("MEALIE_BASE_URL")
    token = os.getenv("MEALIE_TOKEN")
    verify = to_boolean(os.getenv("MEALIE_SSL_VERIFY", "False"))
    if not base_url:
        raise RuntimeError("MEALIE_BASE_URL not set")
    return Api(base_url=base_url, token=token, verify=verify)
