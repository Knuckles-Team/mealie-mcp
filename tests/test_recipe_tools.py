"""Synthetic contracts for discoverable recipe writes; no live Mealie required."""

import json
from unittest.mock import Mock

import pytest
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.recipe_tools import add_recipe_write_tools


@pytest.fixture
def recipe_server(monkeypatch):
    client = Mock()
    client.post_recipes.return_value = "synthetic-soup"
    for method in (
        "put_recipes_slug",
        "patch_one",
        "post_foods",
        "post_units",
        "get_foods",
        "get_units",
    ):
        getattr(client, method).return_value = {"ok": True}
    monkeypatch.setattr("mealie_mcp.recipe_tools.get_client", lambda: client)
    server = FastMCP("synthetic recipe tests")
    add_recipe_write_tools(server)
    return server, client


async def test_discover_nested_schema(recipe_server):
    server, _ = recipe_server
    async with Client(server) as client:
        tools = {tool.name: tool for tool in await client.list_tools()}
    assert len(tools) == 7
    schema = tools["mealie_recipe_patch"].input_schema
    assert set(schema["required"]) == {"slug", "data"}
    assert "params_json" not in schema["properties"]
    encoded = json.dumps(schema)
    for field in (
        "recipeIngredient",
        "quantity",
        "originalText",
        "referenceId",
        "substitutions",
    ):
        assert field in encoded
    assert "section heading" in encoded
    for model in (
        "IngredientFood",
        "CreateIngredientFood",
        "IngredientUnit",
        "CreateIngredientUnit",
    ):
        assert model in encoded


async def test_native_creation_then_patch(recipe_server):
    server, api = recipe_server
    data = {
        "description": None,
        "recipeIngredient": [
            {
                "quantity": 2,
                "food": {"name": "Synthetic carrot"},
                "unit": {"name": "cup"},
                "title": "Soup",
                "note": "diced",
            }
        ],
    }
    async with Client(server) as client:
        result = await client.call_tool(
            "mealie_recipe_create", {"data": {"name": "Synthetic soup"}}
        )
        assert "synthetic-soup" in str(result)
        api.patch_one.assert_not_called()
        await client.call_tool(
            "mealie_recipe_patch", {"slug": "synthetic-soup", "data": data}
        )
    api.post_recipes.assert_called_once_with(data={"name": "Synthetic soup"})
    api.patch_one.assert_called_once_with(slug="synthetic-soup", data=data)


@pytest.mark.parametrize(
    "data",
    [
        {"recipeIngredient": [{"food": "bare-id"}]},
        {"recipeIngredient": [{"unit": {"id": "bad-uuid", "name": "cup"}}]},
        {"recipeIngredient": [{"quantity": "two"}]},
        {"recipeIngredient": [{"quanity": 1}]},
        {"recipeIngredient": [{"food": {"description": "missing name"}}]},
        {"recipeIngredient": "not-an-array"},
        {"recipeIngredient": [{"substitutions": [{"substituteFoodId": "bad-uuid"}]}]},
    ],
)
async def test_invalid_nested_input_never_reaches_api(recipe_server, data):
    server, api = recipe_server
    async with Client(server) as client:
        with pytest.raises(ToolError):
            await client.call_tool(
                "mealie_recipe_patch", {"slug": "synthetic-soup", "data": data}
            )
    api.patch_one.assert_not_called()


async def test_existing_records_and_uuid_roundtrip(recipe_server):
    server, api = recipe_server
    uid = "00000000-0000-4000-8000-000000000001"
    data = {
        "recipeIngredient": [
            {
                "referenceId": uid,
                "food": {"id": uid, "name": "Carrot"},
                "unit": {"id": uid, "name": "cup"},
            }
        ]
    }
    async with Client(server) as client:
        await client.call_tool(
            "mealie_recipe_update", {"slug": "synthetic-soup", "data": data}
        )
    api.put_recipes_slug.assert_called_once_with(slug="synthetic-soup", data=data)


@pytest.mark.parametrize(
    "tool,method,arguments,expected",
    [
        (
            "foods",
            "get_foods",
            {"search": "carrot"},
            {"search": "carrot", "page": 1, "per_page": 50},
        ),
        (
            "units",
            "get_units",
            {"search": "cup", "page": 2},
            {"search": "cup", "page": 2, "per_page": 50},
        ),
        (
            "food_create",
            "post_foods",
            {"data": {"name": "Carrot"}},
            {"data": {"name": "Carrot"}},
        ),
        (
            "unit_create",
            "post_units",
            {"data": {"name": "cup"}},
            {"data": {"name": "cup"}},
        ),
    ],
)
async def test_discovery_and_creation_dispatch(
    recipe_server, tool, method, arguments, expected
):
    server, api = recipe_server
    async with Client(server) as client:
        await client.call_tool("mealie_recipe_" + tool, arguments)
    getattr(api, method).assert_called_once_with(**expected)


async def test_shared_surface_keeps_legacy_and_tags_typed_tools(monkeypatch):
    from agent_connector_sdk.mcp.tool_surface import register_tool_surface

    from mealie_mcp.mcp_server import register_recipes_tools

    monkeypatch.setattr(
        "agent_connector_sdk.mcp.tool_surface.setting", lambda key, default=None: default
    )
    server = FastMCP("surface contract")
    register_tool_surface(
        server,
        service="mealie-mcp",
        registrars=[("recipes", "RECIPESTOOL", register_recipes_tools)],
    )
    assert server._condensed_tool_toggles["mealie_recipe_patch"] == "RECIPESTOOL"
    assert server._condensed_tool_toggles["mealie_recipes"] == "RECIPESTOOL"
    assert {"mealie_recipe_patch", "mealie_recipes"} <= server._intent_gated_tools
    async with Client(server) as client:
        tools = {tool.name: tool for tool in await client.list_tools()}
    legacy = tools["mealie_recipes"].input_schema["properties"]
    assert "action" in legacy and "params_json" in legacy


def test_generated_fields_track_pinned_models():
    from pathlib import Path

    from mealie_mcp import recipe_models

    document = json.loads(
        (Path(__file__).parents[1] / "schemas/recipe-inputs.openapi.json").read_text()
    )
    for name, schema in document["components"]["schemas"].items():
        if name in {"HTTPValidationError", "ValidationError"}:
            continue
        expected = set(schema.get("properties", {}))
        if "update_at" in expected:
            expected.remove("update_at")
            expected.add("updatedAt")
        model = getattr(recipe_models, name)
        assert set(model.model_fields) == expected
        assert {
            name for name, field in model.model_fields.items() if field.is_required()
        } == {
            "updatedAt" if field == "update_at" else field
            for field in schema.get("required", [])
        }


async def test_disabled_recipes_domain_registers_no_typed_or_legacy_tools(monkeypatch):
    from agent_connector_sdk.mcp.tool_surface import register_tool_surface

    from mealie_mcp.mcp_server import register_recipes_tools

    monkeypatch.setattr(
        "agent_connector_sdk.mcp.tool_surface.setting",
        lambda key, default=None: False if key == "RECIPESTOOL" else default,
    )
    server = FastMCP("disabled recipes")
    register_tool_surface(
        server,
        service="mealie-mcp",
        registrars=[("recipes", "RECIPESTOOL", register_recipes_tools)],
    )
    async with Client(server) as client:
        assert await client.list_tools() == []


# REMOVED (SDK-CONNECTOR-CONTROL-R009/R020 migration): this test asserted
# mode_override="intent" deferred a typed tool's registration until the
# multiplexer explicitly revealed it. agent_connector_sdk.mcp.tool_surface
# has no mode parameter at all — register_tool_surface always registers the
# condensed, GATED_TAG-tagged surface (agent-utilities#54's one condensed
# intent contract); deferred-until-revealed registration is not a behavior
# the SDK reproduces, so the premise this test checked no longer holds.
# agent_utilities.mcp.multiplexer itself has no agent_connector_sdk
# equivalent yet (same documented gap as agent_server.py).
