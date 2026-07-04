"""Native epistemic-graph ingestion for Mealie records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The mealie-mcp package natively
pushes its data into the ONE epistemic-graph knowledge graph as **typed OWL nodes**
(``:Recipe``, ``:Ingredient``, ``:Food``, ``:Unit``, ``:RecipeCategory``, ``:Tag``,
``:RecipeTool``) + links, matching the classes federated by ``mealie_mcp.ontology``.

This is a thin mapper over the shared primitive
``agent_utilities.knowledge_graph.memory.native_ingest``. The import is GUARDED: if the
shared primitive is not present in the installed agent_utilities (it is being rolled out
fleet-wide), we fall back to a small self-contained txn writer over the lightweight
engine client. Everything is best-effort and engine-guarded: with no KG stack or no
reachable engine every entry point **no-ops** (returns ``None``), so the connector keeps
working with zero KG infrastructure. Node ids follow ``mealie:<class>:<externalId>``.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("mealie_mcp.kg")

_SOURCE = "mealie-mcp"
_DOMAIN = "mealie"
_DEFAULT_GRAPH = "__commons__"


# --- shared primitive with self-contained fallback -------------------------------------


def _native_client() -> tuple[Any | None, str]:
    """Return ``(engine_client, graph_name)`` or ``(None, "")`` when unavailable."""
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("mealie KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        return client, (getattr(engine, "graph_name", None) or _DEFAULT_GRAPH)
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("mealie KG ingest: engine unreachable: %s", e)
        return None, ""


def _fallback_write(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None,
    *,
    client: Any,
    graph: str,
) -> dict[str, int] | None:
    """Self-contained txn writer (used when the shared primitive is not installed)."""
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None
    try:
        txn = client.txn.begin(graph=graph)
        for ent in entities:
            props = {k: v for k, v in ent.items() if k != "id" and v is not None}
            props.setdefault("source", _SOURCE)
            props.setdefault("domain", _DOMAIN)
            client.txn.add_node(txn, ent["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("mealie KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("mealie KG ingest: txn not committed (conflict)")
        return None

    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("mealie KG ingest: edge skipped: %s", e)
    logger.info("mealie KG ingest: wrote %d nodes, %d edges", len(entities), edges)
    return {"nodes": len(entities), "edges": edges}


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into epistemic-graph.

    Prefers the shared ``native_ingest.ingest_entities`` primitive; falls back to a
    self-contained txn writer when it is not installed. ``client``/``graph`` may be
    injected (tests); otherwise resolved on demand. Returns ``{"nodes":n,"edges":m}``
    or ``None`` (no engine / empty / failure; never raises).
    """
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None

    if client is None:
        try:
            from agent_utilities.knowledge_graph.memory.native_ingest import (
                ingest_entities as _shared_ingest,
            )

            return _shared_ingest(
                entities,
                relationships,
                source=source,
                domain=domain,
                graph=graph,
            )
        except Exception as e:  # noqa: BLE001 — primitive absent / failed, fall back
            logger.debug("mealie KG ingest: shared primitive unavailable: %s", e)
            client, graph = _native_client()

    if client is None:
        return None
    return _fallback_write(
        entities, relationships, client=client, graph=graph or _DEFAULT_GRAPH
    )


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write recipe text as ``:Document`` nodes (semantic-search fodder), best-effort."""
    documents = [d for d in (documents or []) if d.get("id") and d.get("text")]
    if not documents:
        return None
    try:
        from agent_utilities.knowledge_graph.memory.native_ingest import (
            ingest_documents as _shared_docs,
        )

        return _shared_docs(
            documents, source=source, domain=domain, client=client, graph=graph
        )
    except Exception as e:  # noqa: BLE001 — primitive absent, map to :Document nodes
        logger.debug("mealie KG ingest: shared doc primitive unavailable: %s", e)
    nodes: list[dict[str, Any]] = []
    for doc in documents:
        node = {k: v for k, v in doc.items() if v is not None}
        node["type"] = "Document"
        nodes.append(node)
    if client is None:
        client, graph = _native_client()
    if client is None:
        return None
    return _fallback_write(nodes, None, client=client, graph=graph or _DEFAULT_GRAPH)


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
            "type": "Recipe",
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
            {"id": f"mealie:household:{hid}", "type": "Household", "mealieId": hid}
        )
        relationships.append(
            {
                "source": recipe_node_id,
                "target": f"mealie:household:{hid}",
                "type": "inHousehold",
            }
        )
    uid = _str_id(recipe.get("userId"))
    if uid is not None:
        entities.append(
            {"id": f"mealie:person:{uid}", "type": "Person", "mealieId": uid}
        )
        relationships.append(
            {
                "source": recipe_node_id,
                "target": f"mealie:person:{uid}",
                "type": "createdBy",
            }
        )

    for cat in recipe.get("recipeCategory") or []:
        cid = _str_id(cat.get("id")) if isinstance(cat, dict) else None
        if cid is None:
            continue
        entities.append(
            {
                "id": f"mealie:category:{cid}",
                "type": "RecipeCategory",
                "name": cat.get("name"),
                "slug": cat.get("slug"),
                "mealieId": cid,
            }
        )
        relationships.append(
            {
                "source": recipe_node_id,
                "target": f"mealie:category:{cid}",
                "type": "hasCategory",
            }
        )

    for tag in recipe.get("tags") or []:
        tid = _str_id(tag.get("id")) if isinstance(tag, dict) else None
        if tid is None:
            continue
        entities.append(
            {
                "id": f"mealie:tag:{tid}",
                "type": "Tag",
                "name": tag.get("name"),
                "slug": tag.get("slug"),
                "mealieId": tid,
            }
        )
        relationships.append(
            {"source": recipe_node_id, "target": f"mealie:tag:{tid}", "type": "hasTag"}
        )

    for tool in recipe.get("tools") or []:
        tlid = _str_id(tool.get("id")) if isinstance(tool, dict) else None
        if tlid is None:
            continue
        entities.append(
            {
                "id": f"mealie:tool:{tlid}",
                "type": "RecipeTool",
                "name": tool.get("name"),
                "slug": tool.get("slug"),
                "mealieId": tlid,
            }
        )
        relationships.append(
            {
                "source": recipe_node_id,
                "target": f"mealie:tool:{tlid}",
                "type": "usesTool",
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
                "type": "Ingredient",
                "note": ing.get("note"),
                "quantity": ing.get("quantity"),
                "display": ing.get("display"),
                "foodName": (food or {}).get("name"),
                "unitName": (unit or {}).get("name"),
            }
        )
        relationships.append(
            {"source": recipe_node_id, "target": ing_id, "type": "hasIngredient"}
        )
        if food and food.get("id") is not None:
            fid = _str_id(food.get("id"))
            entities.append(
                {
                    "id": f"mealie:food:{fid}",
                    "type": "Food",
                    "name": food.get("name"),
                    "mealieId": fid,
                }
            )
            relationships.append(
                {"source": ing_id, "target": f"mealie:food:{fid}", "type": "usesFood"}
            )
        if unit and unit.get("id") is not None:
            unid = _str_id(unit.get("id"))
            entities.append(
                {
                    "id": f"mealie:unit:{unid}",
                    "type": "Unit",
                    "name": unit.get("name"),
                    "mealieId": unid,
                }
            )
            relationships.append(
                {
                    "source": ing_id,
                    "target": f"mealie:unit:{unid}",
                    "type": "measuredIn",
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
