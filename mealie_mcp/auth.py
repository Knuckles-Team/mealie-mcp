"""Authentication module for mealie-mcp."""

import logging

from agent_connector_sdk.config import setting
from agent_connector_sdk.tls.resolve import resolve_tls_profile

from mealie_mcp.api_client import Api

logger = logging.getLogger(__name__)


def get_client():
    """Get authenticated client for mealie-mcp."""
    base_url = setting("MEALIE_BASE_URL", None)
    token = setting("MEALIE_TOKEN", None)
    if not base_url:
        raise RuntimeError("MEALIE_BASE_URL not set")
    return Api(
        base_url=base_url,
        token=token,
        tls_profile=resolve_tls_profile("mealie"),
    )
