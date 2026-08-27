"""Characterization tests for lane CXA-FL-MEALIEMCP-01.

Pins the CURRENT behavior of the four worst-CCN dispatch-function instances
(all CCN 70) before their extract-method refactor:

  - ``register_households_tools.mealie_households`` in ``mealie_mcp/mcp_server.py``
  - ``register_recipes_tools.mealie_recipes`` in ``mealie_mcp/mcp_server.py``
  - ``register_recipes_tools.mealie_recipes`` in ``mealie_mcp/mcp/mcp_recipes.py``
  - ``register_households_tools.mealie_households`` in ``mealie_mcp/mcp/mcp_households.py``

The two files under ``mealie_mcp/mcp/`` are byte-identical duplicate function
bodies (confirmed via diff) that are never imported by anything outside their
own subpackage (confirmed via workspace-wide grep + the package's entry point,
which is ``mealie_mcp.mcp_server:mcp_server`` — orphaned dead code, reported
in the lane report, NOT deleted here).

These pin several systemic behaviors that are preserved (NOT fixed) by the
refactor and are separately written up as BUGS FOUND in
``plans/complex/lane-reports/CXA-FL-MEALIEMCP-01.md``:

  1. ``ctx.info("Executing tool...")`` is called but never awaited —
     ``fastmcp.Context.info`` is a coroutine function, so this line creates a
     coroutine object that is immediately discarded. Progress reporting is a
     silent no-op and Python raises "coroutine was never awaited".
  2. A JSON payload that decodes to something other than a dict (e.g. a JSON
     array or a bare number) crashes with an uncaught ``AttributeError`` from
     ``kwargs.items()`` — the ``try/except`` only wraps ``json.loads``, not
     the ``.items()`` call, so this is not turned into a graceful error
     response.
  3. An explicit JSON ``null`` value for any params_json key is silently
     stripped before being forwarded to the underlying client method.

Must stay byte-identical between commit 1 (characterize) and commit 2
(refactor); only the three owned implementation files may change between the
two commits.
"""

import asyncio
import json
import warnings

import pytest
from unittest.mock import AsyncMock, MagicMock

from mealie_mcp.mcp_server import (
    VALID_HOUSEHOLDS_ACTIONS as SERVER_HOUSEHOLDS_ACTIONS,
    VALID_RECIPES_ACTIONS as SERVER_RECIPES_ACTIONS,
    register_households_tools as server_register_households_tools,
    register_recipes_tools as server_register_recipes_tools,
)
from mealie_mcp.mcp.mcp_households import (
    VALID_HOUSEHOLDS_ACTIONS as MIRROR_HOUSEHOLDS_ACTIONS,
    register_households_tools as mirror_register_households_tools,
)
from mealie_mcp.mcp.mcp_recipes import (
    VALID_RECIPES_ACTIONS as MIRROR_RECIPES_ACTIONS,
    register_recipes_tools as mirror_register_recipes_tools,
)

TARGETS = [
    pytest.param(
        server_register_households_tools, SERVER_HOUSEHOLDS_ACTIONS, id="server_households"
    ),
    pytest.param(
        server_register_recipes_tools, SERVER_RECIPES_ACTIONS, id="server_recipes"
    ),
    pytest.param(
        mirror_register_households_tools, MIRROR_HOUSEHOLDS_ACTIONS, id="mirror_households"
    ),
    pytest.param(
        mirror_register_recipes_tools, MIRROR_RECIPES_ACTIONS, id="mirror_recipes"
    ),
]


class _CaptureMCP:
    """Stand-in FastMCP that captures the registered tool callable."""

    def __init__(self):
        self.fns = []

    def tool(self, *args, **kwargs):
        def decorator(fn):
            self.fns.append(fn)
            return fn

        return decorator


def _register(register_fn):
    cap = _CaptureMCP()
    register_fn(cap)
    assert len(cap.fns) == 1, "expected exactly one tool registered"
    return cap.fns[0]


@pytest.mark.parametrize("register_fn,actions", TARGETS)
def test_every_action_calls_the_same_named_client_method(register_fn, actions):
    """Every documented action routes to a client method of the identical
    name, and every non-null kwarg is forwarded through unchanged."""
    fn = _register(register_fn)
    assert len(actions) > 0
    for action in actions:
        mock_client = MagicMock()
        payload = {"item_id": "abc123", "page": 0, "explicit_null": None}
        result = asyncio.run(
            fn(
                action=action,
                params_json=json.dumps(payload),
                client=mock_client,
                ctx=None,
            )
        )
        method = getattr(mock_client, action)
        method.assert_called_once_with(item_id="abc123", page=0)
        assert "explicit_null" not in method.call_args.kwargs
        assert result is method.return_value


@pytest.mark.parametrize("register_fn,actions", TARGETS)
def test_action_count_matches_branch_count(register_fn, actions):
    """No unhandled action, no unreachable/duplicate branch: every action in
    the manifest is handled without raising ValueError."""
    fn = _register(register_fn)
    for action in actions:
        mock_client = MagicMock()
        asyncio.run(fn(action=action, params_json="{}", client=mock_client, ctx=None))


@pytest.mark.parametrize("register_fn,actions", TARGETS)
def test_unknown_action_raises_resolve_actions_rich_error(register_fn, actions):
    """FINDING (reported, not fixed): the function's own trailing
    ``raise ValueError(f"Unknown action: {action}")`` is unreachable dead
    code. ``resolve_action(...)`` is called first and always either returns a
    valid canonical action name or raises its own rich
    "Unknown action '<x>' on <service>. ... Call with action='list_actions'
    ..." ValueError before the if/elif chain (and its trailing raise) is ever
    reached. This pins the REAL (resolve_action's) message, not the
    unreachable one."""
    fn = _register(register_fn)
    mock_client = MagicMock()
    with pytest.raises(ValueError, match=r"^Unknown action '__nope__' on mealie-mcp\."):
        asyncio.run(
            fn(action="__nope__", params_json="{}", client=mock_client, ctx=None)
        )
    mock_client.assert_not_called()


@pytest.mark.parametrize("register_fn,actions", TARGETS)
def test_invalid_json_returns_generic_error_and_swallows_cause(register_fn, actions):
    """BUG (pinned, not fixed in this lane): the real json.JSONDecodeError is
    discarded and replaced with a generic message. See BUGS FOUND in the lane
    report."""
    fn = _register(register_fn)
    mock_client = MagicMock()
    result = asyncio.run(
        fn(
            action=actions[0],
            params_json="{not-json",
            client=mock_client,
            ctx=None,
        )
    )
    assert result == {"error": "Operation failed"}
    mock_client.assert_not_called()


@pytest.mark.parametrize("register_fn,actions", TARGETS)
def test_non_object_json_crashes_uncaught(register_fn, actions):
    """BUG (pinned, not fixed in this lane): a JSON array (or any non-dict
    JSON value) is NOT rejected gracefully — ``kwargs.items()`` is called
    outside the try/except that wraps ``json.loads``, so this raises a raw
    AttributeError straight out of the tool function. See BUGS FOUND."""
    fn = _register(register_fn)
    mock_client = MagicMock()
    with pytest.raises(AttributeError, match="items"):
        asyncio.run(
            fn(
                action=actions[0],
                params_json="[1, 2, 3]",
                client=mock_client,
                ctx=None,
            )
        )
    mock_client.assert_not_called()


@pytest.mark.parametrize("register_fn,actions", TARGETS)
def test_empty_params_json_defaults_to_empty_kwargs(register_fn, actions):
    fn = _register(register_fn)
    mock_client = MagicMock()
    action = actions[0]
    asyncio.run(fn(action=action, params_json="{}", client=mock_client, ctx=None))
    getattr(mock_client, action).assert_called_once_with()


@pytest.mark.parametrize("register_fn,actions", TARGETS)
def test_ctx_info_is_called_but_never_awaited(register_fn, actions):
    """BUG (pinned, not fixed in this lane): ``ctx.info(...)`` is a coroutine
    function (fastmcp.Context.info is async) but is invoked without
    ``await``. The call happens (the mock records it) but the coroutine is
    never awaited, so it never actually runs, and Python emits
    "coroutine was never awaited". See BUGS FOUND."""
    fn = _register(register_fn)
    mock_client = MagicMock()
    ctx = AsyncMock()
    action = actions[0]
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        asyncio.run(fn(action=action, params_json="{}", client=mock_client, ctx=ctx))
    assert ctx.info.called, "ctx.info(...) should still be invoked (call happens)"
    assert ctx.info.await_count == 0, "ctx.info(...) is never actually awaited"
    assert any(
        issubclass(w.category, RuntimeWarning) and "never awaited" in str(w.message)
        for w in caught
    ), "expected a 'coroutine ... was never awaited' RuntimeWarning"


@pytest.mark.parametrize("register_fn,actions", TARGETS)
def test_ctx_none_skips_progress_reporting(register_fn, actions):
    fn = _register(register_fn)
    mock_client = MagicMock()
    action = actions[0]
    # Must not raise even though ctx is None (falsy branch of "if ctx:").
    asyncio.run(fn(action=action, params_json="{}", client=mock_client, ctx=None))


def test_server_and_mirror_households_action_sets_are_identical():
    """The mcp_server.py and mcp/mcp_households.py copies list the exact
    same 64 valid actions (they are byte-identical duplicate bodies)."""
    assert set(SERVER_HOUSEHOLDS_ACTIONS) == set(MIRROR_HOUSEHOLDS_ACTIONS)
    assert len(SERVER_HOUSEHOLDS_ACTIONS) == 64


def test_server_and_mirror_recipes_action_sets_are_identical():
    """The mcp_server.py and mcp/mcp_recipes.py copies list the exact same
    64 valid actions (they are byte-identical duplicate bodies)."""
    assert set(SERVER_RECIPES_ACTIONS) == set(MIRROR_RECIPES_ACTIONS)
    assert len(SERVER_RECIPES_ACTIONS) == 64
