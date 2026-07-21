"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_recipes`` seam with a fake
ChangeEnvelope-capable engine client (no engine required; the same fake shape as
agent-utilities' own ``tests/knowledge_graph/test_native_ingest.py``), asserting the
governed-session transaction commit and the Mealie recipe ->
:Recipe/:Ingredient/:Food/:Unit/:RecipeCategory/:Tag mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from typing import Any

import msgpack
import pytest
from agent_utilities.knowledge_graph.core.session import GraphSession, use_session
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError
from agent_utilities.models.company_brain import ActorType
from agent_utilities.security.brain_context import ActorContext, use_actor

from mealie_mcp.kg_ingest import ingest_entities, ingest_recipes, map_recipe


@pytest.fixture(autouse=True)
def _governed_session():
    """Every native-ingest call must inherit an authenticated ambient GraphSession."""
    actor = ActorContext(
        actor_id="subject:opaque:synthetic",
        actor_type=ActorType.AUTOMATED_SERVICE,
        roles=(),
        tenant_id="tenant:opaque:synthetic",
        authenticated=True,
    )
    session = GraphSession(
        actor=actor,
        tenant=actor.tenant_id,
        scopes=frozenset({"kg:write"}),
        graph="graph:opaque:synthetic",
        policy_version="policy:opaque:synthetic",
        audience="epistemic-graph",
    )
    with use_actor(actor), use_session(session):
        yield


class _FakeNodes:
    def __init__(self) -> None:
        self.values: dict[str, dict[str, Any]] = {}

    def properties(self, node_id: str) -> dict[str, Any] | None:
        return self.values.get(node_id)

    def list(self) -> list[tuple[str, dict[str, Any]]]:
        return list(self.values.items())


class _FakeChanges:
    def __init__(self, nodes: _FakeNodes) -> None:
        self.nodes = nodes
        self.edges: list[tuple[str, str, dict[str, Any]]] = []
        self.applied: list[dict[str, Any]] = []
        self.records: dict[str, dict[str, Any]] = {}
        self.versions: dict[str, dict[str, Any]] = {}

    def get(self, envelope_id: str) -> dict[str, Any] | None:
        return self.records.get(envelope_id)

    def content_version(self, object_id: str) -> dict[str, Any] | None:
        return self.versions.get(object_id)

    def cursor(self, _source: str, _partition: str = "") -> None:
        return None

    def apply(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(envelope)
        mutation = envelope["mutation"]
        for operation in mutation["operations"]:
            method = operation["method"]
            params = method["params"]
            properties = msgpack.unpackb(params["properties_msgpack"], raw=False)
            if method["method"] == "AddNode":
                self.nodes.values[params["node_id"]] = properties
            elif method["method"] == "AddEdge":
                self.edges.append(
                    (params["source_id"], params["target_id"], properties)
                )
        version = envelope["content_version"]
        self.versions[version["object_id"]] = version
        self.records[envelope["envelope_id"]] = envelope
        return {
            "batch_id": mutation["batch_id"],
            "replayed": False,
            "projection_pending": False,
        }


class _FakeRdf:
    def validate_shacl(self, _shapes: str, _data_graph: str) -> dict[str, Any]:
        return {"conforms": True, "results": []}


class _FakeClient:
    def __init__(self) -> None:
        self.nodes = _FakeNodes()
        self.changes = _FakeChanges(self.nodes)
        self.rdf = _FakeRdf()

    @staticmethod
    def supports(operation: str) -> bool:
        return operation == "ApplyChangeEnvelope"


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


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Recipe", "name": "p"},
            {"id": "b", "node_type": "RecipeCategory"},
        ],
        [{"source": "a", "target": "b", "relationship": "hasCategory"}],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert set(c.nodes.values) == {"a", "b"}
    # provenance is stamped
    assert c.nodes.values["a"]["source"] == "mealie-mcp"
    assert c.nodes.values["a"]["domain"] == "mealie"
    assert c.changes.edges == [("a", "b", {"relationship": "hasCategory"})]


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


def test_ingest_recipes_maps_and_writes():
    c = _FakeClient()
    res = ingest_recipes([_FULL_RECIPE], client=c)
    assert res is not None
    assert c.nodes.values["mealie:recipe:r-1"]["node_type"] == "Recipe"
    assert c.nodes.values["mealie:recipe:r-1"]["externalToolId"] == "r-1"
    # ingredient food/unit edges were added
    assert (
        "mealie:ingredient:r-1:ing-1",
        "mealie:food:f-1",
        {"relationship": "usesFood"},
    ) in c.changes.edges


def test_ingest_recipes_summary_shape():
    """A list-shaped summary (no recipeIngredient) still maps the recipe + labels."""
    c = _FakeClient()
    summary = {
        "id": "r-2",
        "name": "Chili",
        "slug": "chili",
        "tags": [{"id": "t-1", "name": "Spicy", "slug": "spicy"}],
    }
    res = ingest_recipes([summary], client=c)
    assert res == {"nodes": 2, "edges": 1}
    assert c.nodes.values["mealie:recipe:r-2"]["node_type"] == "Recipe"
    assert c.nodes.values["mealie:tag:t-1"]["node_type"] == "Tag"


def test_retired_structural_alias_is_rejected():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities([{"id": "a", "type": "Recipe"}], client=_FakeClient())


def test_empty_native_ingest_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())
