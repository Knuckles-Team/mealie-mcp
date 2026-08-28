"""Regression test for BUG-CX-046: ``ctx.info(...)`` called without ``await``.

``fastmcp.Context.info`` is an async coroutine method. Throughout
``mealie_mcp/mcp/mcp_*.py`` and ``mealie_mcp/mcp_server.py``, tool functions
contain the pattern::

    if ctx:
        ctx.info("Executing tool...")

Calling a coroutine method without ``await`` creates a coroutine object that
is immediately discarded -- the log line never actually emits, and Python
raises ``RuntimeWarning: coroutine 'Context.info' was never awaited``. The
fix is to add ``await``.

This test picks one representative tool function (``mealie_groups`` in
``mealie_mcp/mcp/mcp_groups.py``), registers it the same way this repo's
other characterization tests do (a stand-in ``FastMCP``-like object whose
``.tool()`` decorator just captures the wrapped callable -- see
``tests/test_cxa_fl_mealiemcp_01_characterization.py``), and proves that
``ctx.info(...)`` is actually awaited when the tool runs.

Before the fix: ``ctx.info.await_count`` stays 0 (the call happens but is
never awaited) and a "coroutine ... was never awaited" RuntimeWarning fires.
After the fix: the mock is awaited exactly once and no such warning fires.
"""

import asyncio
import warnings
from unittest.mock import AsyncMock, MagicMock

from mealie_mcp.mcp.mcp_groups import register_groups_tools


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


def test_ctx_info_is_awaited_on_mealie_groups():
    """BUG-CX-046: ``ctx.info(...)`` must be awaited, not fire-and-forget."""
    fn = _register(register_groups_tools)
    mock_client = MagicMock()
    ctx = AsyncMock()

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        asyncio.run(
            fn(
                action="get_all_households",
                params_json="{}",
                client=mock_client,
                ctx=ctx,
            )
        )

    ctx.info.assert_awaited_once_with("Executing tool...")
    assert not any(
        issubclass(w.category, RuntimeWarning) and "never awaited" in str(w.message)
        for w in caught
    ), "ctx.info(...) coroutine must not be left un-awaited"
