"""Native epistemic-graph ingestion for Mealie records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The mealie-mcp package natively
pushes its data into the ONE epistemic-graph knowledge graph as **typed OWL nodes**
(``:Recipe``, ``:Ingredient``, ``:Food``, ``:Unit``, ``:RecipeCategory``, ``:Tag``,
``:RecipeTool``) + links, matching the classes federated by ``mealie_mcp.ontology``.

This is a thin mapper over the required
``agent_utilities.knowledge_graph.memory.native_ingest`` transaction primitive. Engine
failures are explicit, and partial writes are never acknowledged. Node ids follow
``mealie:<class>:<externalId>``.
"""

from __future__ import annotations

import logging
from typing import Any

from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_documents as _native_ingest_documents,
)
from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_entities as _native_ingest_entities,
)

logger = logging.getLogger("mealie_mcp.kg")

_SOURCE = "mealie-mcp"
_DOMAIN = "mealie"
def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write typed OWL nodes (+ edges) into epistemic-graph.

    Nodes use ``node_type`` and relationships use ``relationship``. ``client``/``graph``
    may be injected for isolated validation.
    """
    return _native_ingest_entities(
        entities,
        relationships,
        source=source,
        domain=domain,
        client=client,
        graph=graph,
    )


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write recipe text as canonical ``:Document`` nodes."""
    return _native_ingest_documents(
        documents,
        source=source,
        domain=domain,
        client=client,
        graph=graph,
    )


# --- domain mappers --------------------------------------------------------------------


def _str_id(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def map_recipe(
    recipe: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Map ONE Mealie recipe record → entities + relationships.

    Handles both the list-shaped summary (``get_recipes`` items) and the full
    single-recipe body (``get_recipes_slug``, which additionally carries
    ``recipeIngredient``). Returns ``(entities, relationships)``.
    """
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []

    rid = _str_id(recipe.get("id"))
    if rid is None:
        return entities, relationships
    recipe_node_id = f"mealie:recipe:{rid}"

    entities.append(
        {
            "id": recipe_node_id,
            "node_type": "Recipe",
            "name": recipe.get("name"),
            "slug": recipe.get("slug"),
            "description": recipe.get("description"),
            "recipeYield": recipe.get("recipeYield"),
            "prepTime": recipe.get("prepTime"),
            "cookTime": recipe.get("performTime") or recipe.get("cookTime"),
            "totalTime": recipe.get("totalTime"),
            "rating": recipe.get("rating"),
            "dateAdded": recipe.get("dateAdded"),
            "updated_at": recipe.get("updateAt") or recipe.get("dateUpdated"),
            "mealieId": rid,
            "externalToolId": rid,
        }
    )

    # household link (Person authorship via userId, household via householdId)
    hid = _str_id(recipe.get("householdId"))
    if hid is not None:
        entities.append(
            {"id": f"mealie:household:{hid}", "node_type": "Household", "mealieId": hid}
        )
        relationships.append(
            {
                "source": recipe_node_id,
                "target": f"mealie:household:{hid}",
                "relationship": "inHousehold",
            }
        )
    uid = _str_id(recipe.get("userId"))
    if uid is not None:
        entities.append(
            {"id": f"mealie:person:{uid}", "node_type": "Person", "mealieId": uid}
        )
        relationships.append(
            {
                "source": recipe_node_id,
                "target": f"mealie:person:{uid}",
                "relationship": "createdBy",
            }
        )

    for cat in recipe.get("recipeCategory") or []:
        cid = _str_id(cat.get("id")) if isinstance(cat, dict) else None
        if cid is None:
            continue
        entities.append(
            {
                "id": f"mealie:category:{cid}",
                "node_type": "RecipeCategory",
                "name": cat.get("name"),
                "slug": cat.get("slug"),
                "mealieId": cid,
            }
        )
        relationships.append(
            {
                "source": recipe_node_id,
                "target": f"mealie:category:{cid}",
                "relationship": "hasCategory",
            }
        )

    for tag in recipe.get("tags") or []:
        tid = _str_id(tag.get("id")) if isinstance(tag, dict) else None
        if tid is None:
            continue
        entities.append(
            {
                "id": f"mealie:tag:{tid}",
                "node_type": "Tag",
                "name": tag.get("name"),
                "slug": tag.get("slug"),
                "mealieId": tid,
            }
        )
        relationships.append(
            {"source": recipe_node_id, "target": f"mealie:tag:{tid}", "relationship": "hasTag"}
        )

    for tool in recipe.get("tools") or []:
        tlid = _str_id(tool.get("id")) if isinstance(tool, dict) else None
        if tlid is None:
            continue
        entities.append(
            {
                "id": f"mealie:tool:{tlid}",
                "node_type": "RecipeTool",
                "name": tool.get("name"),
                "slug": tool.get("slug"),
                "mealieId": tlid,
            }
        )
        relationships.append(
            {
                "source": recipe_node_id,
                "target": f"mealie:tool:{tlid}",
                "relationship": "usesTool",
            }
        )

    for ing in recipe.get("recipeIngredient") or []:
        if not isinstance(ing, dict):
            continue
        ref = _str_id(ing.get("referenceId")) or _str_id(ing.get("note")) or ""
        ing_id = f"mealie:ingredient:{rid}:{ref}" if ref else None
        food = ing.get("food") if isinstance(ing.get("food"), dict) else None
        unit = ing.get("unit") if isinstance(ing.get("unit"), dict) else None
        if ing_id is None:
            continue
        entities.append(
            {
                "id": ing_id,
                "node_type": "Ingredient",
                "note": ing.get("note"),
                "quantity": ing.get("quantity"),
                "display": ing.get("display"),
                "foodName": (food or {}).get("name"),
                "unitName": (unit or {}).get("name"),
            }
        )
        relationships.append(
            {"source": recipe_node_id, "target": ing_id, "relationship": "hasIngredient"}
        )
        if food and food.get("id") is not None:
            fid = _str_id(food.get("id"))
            entities.append(
                {
                    "id": f"mealie:food:{fid}",
                    "node_type": "Food",
                    "name": food.get("name"),
                    "mealieId": fid,
                }
            )
            relationships.append(
                {"source": ing_id, "target": f"mealie:food:{fid}", "relationship": "usesFood"}
            )
        if unit and unit.get("id") is not None:
            unid = _str_id(unit.get("id"))
            entities.append(
                {
                    "id": f"mealie:unit:{unid}",
                    "node_type": "Unit",
                    "name": unit.get("name"),
                    "mealieId": unid,
                }
            )
            relationships.append(
                {
                    "source": ing_id,
                    "target": f"mealie:unit:{unid}",
                    "relationship": "measuredIn",
                }
            )

    return entities, relationships


def ingest_recipes(
    recipes: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Mealie recipe records → typed nodes/links and ingest them in one pass."""
    all_entities: list[dict[str, Any]] = []
    all_relationships: list[dict[str, Any]] = []
    for recipe in recipes or []:
        if not isinstance(recipe, dict):
            continue
        ents, rels = map_recipe(recipe)
        all_entities.extend(ents)
        all_relationships.extend(rels)
    return ingest_entities(all_entities, all_relationships, client=client, graph=graph)
