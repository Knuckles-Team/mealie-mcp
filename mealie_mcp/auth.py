"""Authentication module for mealie-mcp."""

from agent_utilities.base_utilities import get_logger
from agent_utilities.core.config import setting
from agent_utilities.core.transport_security import resolve_configured_tls_profile

from mealie_mcp.api_client import Api

logger = get_logger(__name__)


def get_client():
    """Get authenticated client for mealie-mcp."""
    base_url = setting("MEALIE_BASE_URL", None)
    token = setting("MEALIE_TOKEN", None)
    if not base_url:
        raise RuntimeError("MEALIE_BASE_URL not set")
    return Api(
        base_url=base_url,
        token=token,
        tls_profile=resolve_configured_tls_profile("mealie"),
    )
