"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_recipes`` seam with a fake
transport one level below ``agent_connector_sdk.ingest.KnowledgeIngest`` (no
engine required), so the SDK's own request-building/validation contract runs
unfaked, and asserts the Mealie recipe ->
:Recipe/:Ingredient/:Food/:Unit/:RecipeCategory/:Tag mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import IngestError, KnowledgeIngest

from mealie_mcp.kg_ingest import ingest_entities, ingest_recipes, map_recipe


class _FakeTransport:
    def __init__(self) -> None:
        self.requests: list[Any] = []

    async def source_status(self, connector: str, stream: str):
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request):
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data: bytes) -> str:
        raise AssertionError("this connector's node/edge ingestion carries no media")


@pytest.fixture
def ingest():
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


_FULL_RECIPE = {
    "id": "r-1",
    "name": "Spaghetti Carbonara",
    "slug": "spaghetti-carbonara",
    "description": "Classic Roman pasta.",
    "recipeYield": "4 servings",
    "userId": "u-9",
    "householdId": "h-2",
    "recipeCategory": [{"id": "c-5", "name": "Dinner", "slug": "dinner"}],
    "tags": [{"id": "t-7", "name": "Italian", "slug": "italian"}],
    "tools": [{"id": "tl-3", "name": "Pot", "slug": "pot"}],
    "recipeIngredient": [
        {
            "referenceId": "ing-1",
            "note": "grated",
            "quantity": 100,
            "food": {"id": "f-1", "name": "Pecorino"},
            "unit": {"id": "un-1", "name": "grams"},
        }
    ],
}


async def test_ingest_entities_writes_nodes_and_edges(ingest):
    service, transport = ingest
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "Recipe", "name": "p"},
            {"id": "b", "node_type": "RecipeCategory"},
        ],
        [{"source": "a", "target": "b", "relationship": "hasCategory"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    request = transport.requests[0]
    ids = {record.record_id for record in request.records}
    assert ids == {"a", "b"}
    assert len(request.relationships) == 1


def test_map_recipe_full_body():
    entities, rels = map_recipe(_FULL_RECIPE)
    by_id = {e["id"]: e for e in entities}
    assert by_id["mealie:recipe:r-1"]["node_type"] == "Recipe"
    assert by_id["mealie:recipe:r-1"]["slug"] == "spaghetti-carbonara"
    assert by_id["mealie:category:c-5"]["node_type"] == "RecipeCategory"
    assert by_id["mealie:tag:t-7"]["node_type"] == "Tag"
    assert by_id["mealie:tool:tl-3"]["node_type"] == "RecipeTool"
    assert by_id["mealie:food:f-1"]["node_type"] == "Food"
    assert by_id["mealie:unit:un-1"]["node_type"] == "Unit"
    ing_id = "mealie:ingredient:r-1:ing-1"
    assert by_id[ing_id]["node_type"] == "Ingredient"
    assert by_id[ing_id]["foodName"] == "Pecorino"
    # relationships present
    rel_types = {(r["source"], r["target"], r["relationship"]) for r in rels}
    assert ("mealie:recipe:r-1", ing_id, "hasIngredient") in rel_types
    assert (ing_id, "mealie:food:f-1", "usesFood") in rel_types
    assert (ing_id, "mealie:unit:un-1", "measuredIn") in rel_types
    assert ("mealie:recipe:r-1", "mealie:category:c-5", "hasCategory") in rel_types
    assert ("mealie:recipe:r-1", "mealie:person:u-9", "createdBy") in rel_types
    assert ("mealie:recipe:r-1", "mealie:household:h-2", "inHousehold") in rel_types


async def test_ingest_recipes_maps_and_writes(ingest):
    service, transport = ingest
    res = await ingest_recipes([_FULL_RECIPE], ingest=service)
    assert res is not None
    request = transport.requests[0]
    by_id = {record.record_id: record for record in request.records}
    assert by_id["mealie:recipe:r-1"].mapping_reference.endswith("/Recipe")
    # ingredient food/unit edges were added
    edge_types = {
        (rel.source.record_id, rel.target.record_id, rel.relation_reference.rsplit("/relations/", 1)[-1])
        for rel in request.relationships
    }
    assert ("mealie:ingredient:r-1:ing-1", "mealie:food:f-1", "usesFood") in edge_types


async def test_ingest_recipes_summary_shape(ingest):
    """A list-shaped summary (no recipeIngredient) still maps the recipe + labels."""
    service, transport = ingest
    summary = {
        "id": "r-2",
        "name": "Chili",
        "slug": "chili",
        "tags": [{"id": "t-1", "name": "Spicy", "slug": "spicy"}],
    }
    res = await ingest_recipes([summary], ingest=service)
    assert res == {"nodes": 2, "edges": 1}
    request = transport.requests[0]
    by_id = {record.record_id: record for record in request.records}
    assert by_id["mealie:recipe:r-2"].mapping_reference.endswith("/Recipe")
    assert by_id["mealie:tag:t-1"].mapping_reference.endswith("/Tag")


async def test_retired_structural_alias_is_rejected(ingest):
    service, _ = ingest
    with pytest.raises(IngestError, match="node_type"):
        await ingest_entities([{"id": "a", "type": "Recipe"}], ingest=service)


async def test_empty_native_ingest_is_rejected(ingest):
    service, _ = ingest
    with pytest.raises(IngestError, match="at least one entity"):
        await ingest_entities([], ingest=service)
