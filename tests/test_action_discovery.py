"""Action-discovery behavior for the standardized action-routed tools."""

import pytest
from agent_utilities.mcp.action_dispatch import resolve_action

from mealie_mcp.mcp_server import (
    VALID_ADMIN_ACTIONS,
    VALID_APP_ACTIONS,
    VALID_RECIPES_ACTIONS,
    VALID_USERS_ACTIONS,
)

ACTION_SETS = [
    VALID_APP_ACTIONS,
    VALID_USERS_ACTIONS,
    VALID_RECIPES_ACTIONS,
    VALID_ADMIN_ACTIONS,
]


@pytest.mark.parametrize("valid_actions", ACTION_SETS)
@pytest.mark.parametrize("keyword", ["list_actions", "actions", "help"])
def test_discovery_returns_action_names(valid_actions, keyword):
    """Discovery keywords return a {service, actions} payload listing names."""
    result = resolve_action(keyword, valid_actions, service="mealie-mcp")
    assert isinstance(result, dict)
    assert result["service"] == "mealie-mcp"
    assert set(result["actions"]) == set(valid_actions)


@pytest.mark.parametrize("valid_actions", ACTION_SETS)
def test_canonical_action_passes_through(valid_actions):
    """A valid action resolves to itself."""
    canonical = valid_actions[0]
    assert resolve_action(canonical, valid_actions, service="mealie-mcp") == canonical


@pytest.mark.parametrize("valid_actions", ACTION_SETS)
def test_bogus_action_raises_did_you_mean(valid_actions):
    """An unknown action raises a rich error mentioning list_actions."""
    with pytest.raises(ValueError) as exc:
        resolve_action("totally_bogus_action_xyz", valid_actions, service="mealie-mcp")
    message = str(exc.value)
    assert "list_actions" in message
