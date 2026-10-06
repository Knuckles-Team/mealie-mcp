"""Synthetic endpoint-boundary regressions for typed and legacy recipe tools."""

import inspect
import json
from unittest.mock import Mock
from urllib.parse import unquote, urlsplit

import pytest
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.api.api_client_recipes import Api
from mealie_mcp.mcp_server import register_recipes_tools

UNSAFE_SLUGS = [
    "",
    ".",
    "..",
    "../foods/00000000-0000-4000-8000-000000000001",
    "a/b",
    "a\\b",
    "a?query=1",
    "a#fragment",
    "a\nb",
    "a\tb",
    "a\x00b",
    "%2e%2e",
    "%2E%2E%2Ffoods",
    "%252e%252e%252ffoods",
    "a%2fb",
    "a%5Cb",
    "a%3Fb",
    "a%23b",
    "a%0Ab",
    "a%257fb",
]
SLUG_METHODS = [
    name
    for name, method in inspect.getmembers(Api, inspect.isfunction)
    if "slug" in inspect.signature(method).parameters
]


@pytest.fixture
def api():
    client = Api.__new__(Api)
    client.base_url = "https://synthetic.invalid/"
    client._session = Mock()
    client._session.request.return_value.status_code = 200
    client._session.request.return_value.json.return_value = {"ok": True}
    return client


def arguments(method, slug):
    return {
        name: slug if name == "slug" else {} if name == "data" else "synthetic"
        for name, param in inspect.signature(method).parameters.items()
        if param.default is inspect.Parameter.empty
    }


@pytest.mark.parametrize("slug", UNSAFE_SLUGS)
@pytest.mark.parametrize("name", SLUG_METHODS)
def test_every_recipe_slug_endpoint_rejects_before_network(api, name, slug):
    method = getattr(api, name)
    with pytest.raises(ValueError, match="safe URL path segment"):
        method(**arguments(method, slug))
    api._session.request.assert_not_called()


@pytest.mark.parametrize(
    "slug", ["soup", "Crème brûlée", "50% soup", "a.b", "...", "a+b", "饭"]
)
@pytest.mark.parametrize("name", ["put_recipes_slug", "patch_one"])
def test_explicit_upstream_slugs_stay_in_one_segment(api, name, slug):
    getattr(api, name)(slug=slug, data={"name": "Synthetic soup"})
    url = urlsplit(api._session.request.call_args.kwargs["url"])
    assert url.netloc == "synthetic.invalid"
    assert not url.query and not url.fragment
    assert url.path.rsplit("/", 1)[0] == "/api/recipes"
    assert unquote(url.path.rsplit("/", 1)[1]) == slug


@pytest.mark.parametrize("slug", UNSAFE_SLUGS)
@pytest.mark.parametrize("action", ["put_recipes_slug", "patch_one"])
async def test_typed_and_legacy_tools_cannot_escape_recipe_endpoint(
    api, monkeypatch, slug, action
):
    monkeypatch.setattr("mealie_mcp.mcp_server.get_client", lambda: api)
    monkeypatch.setattr("mealie_mcp.recipe_tools.get_client", lambda: api)
    server = FastMCP("synthetic path tests")
    register_recipes_tools(server)
    tool = (
        "mealie_recipe_update"
        if action == "put_recipes_slug"
        else "mealie_recipe_patch"
    )
    payload = {"slug": slug, "data": {"name": "Synthetic soup"}}
    async with Client(server) as client:
        with pytest.raises(ToolError):
            await client.call_tool(tool, payload)
        # Legacy dispatch may report exceptions in its result; either way no
        # transport call is allowed to occur.
        try:
            await client.call_tool(
                "mealie_recipes", {"action": action, "params_json": json.dumps(payload)}
            )
        except ToolError:
            pass
    api._session.request.assert_not_called()
