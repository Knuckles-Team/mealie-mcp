"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_recipes`` seam with a fake engine
client (no engine required), asserting the txn add_node/commit + edge calls and the
Mealie recipe -> :Recipe/:Ingredient/:Food/:Unit/:RecipeCategory/:Tag mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from mealie_mcp.kg_ingest import ingest_entities, ingest_recipes, map_recipe


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed = True
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


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
            {"id": "a", "type": "Recipe", "name": "p"},
            {"id": "b", "type": "RecipeCategory"},
        ],
        [{"source": "a", "target": "b", "type": "hasCategory"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "mealie-mcp"
    assert c.txn.nodes["a"]["domain"] == "mealie"
    assert c.edges.edges == [("a", "b", {"type": "hasCategory"})]


def test_map_recipe_full_body():
    entities, rels = map_recipe(_FULL_RECIPE)
    by_id = {e["id"]: e for e in entities}
    assert by_id["mealie:recipe:r-1"]["type"] == "Recipe"
    assert by_id["mealie:recipe:r-1"]["slug"] == "spaghetti-carbonara"
    assert by_id["mealie:category:c-5"]["type"] == "RecipeCategory"
    assert by_id["mealie:tag:t-7"]["type"] == "Tag"
    assert by_id["mealie:tool:tl-3"]["type"] == "RecipeTool"
    assert by_id["mealie:food:f-1"]["type"] == "Food"
    assert by_id["mealie:unit:un-1"]["type"] == "Unit"
    ing_id = "mealie:ingredient:r-1:ing-1"
    assert by_id[ing_id]["type"] == "Ingredient"
    assert by_id[ing_id]["foodName"] == "Pecorino"
    # relationships present
    rel_types = {(r["source"], r["target"], r["type"]) for r in rels}
    assert ("mealie:recipe:r-1", ing_id, "hasIngredient") in rel_types
    assert (ing_id, "mealie:food:f-1", "usesFood") in rel_types
    assert (ing_id, "mealie:unit:un-1", "measuredIn") in rel_types
    assert ("mealie:recipe:r-1", "mealie:category:c-5", "hasCategory") in rel_types
    assert ("mealie:recipe:r-1", "mealie:person:u-9", "createdBy") in rel_types
    assert ("mealie:recipe:r-1", "mealie:household:h-2", "inHousehold") in rel_types


def test_ingest_recipes_maps_and_writes():
    c = _FakeClient()
    res = ingest_recipes([_FULL_RECIPE], client=c, graph="__commons__")
    assert res is not None
    assert c.txn.committed is True
    assert c.txn.nodes["mealie:recipe:r-1"]["type"] == "Recipe"
    assert c.txn.nodes["mealie:recipe:r-1"]["externalToolId"] == "r-1"
    # ingredient food/unit edges were added
    assert (
        "mealie:ingredient:r-1:ing-1",
        "mealie:food:f-1",
        {"type": "usesFood"},
    ) in c.edges.edges


def test_ingest_recipes_summary_shape():
    """A list-shaped summary (no recipeIngredient) still maps the recipe + labels."""
    c = _FakeClient()
    summary = {
        "id": "r-2",
        "name": "Chili",
        "slug": "chili",
        "tags": [{"id": "t-1", "name": "Spicy", "slug": "spicy"}],
    }
    res = ingest_recipes([summary], client=c, graph="__commons__")
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.nodes["mealie:recipe:r-2"]["type"] == "Recipe"
    assert c.txn.nodes["mealie:tag:t-1"]["type"] == "Tag"


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op.
    assert ingest_entities([{"id": "a", "type": "Recipe"}]) is None


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_recipes([], client=_FakeClient()) is None
    assert ingest_recipes([{"no_id": 1}], client=_FakeClient()) is None
