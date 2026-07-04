"""Native epistemic-graph blob ingestion for Mealie recipe images.

CONCEPT:AU-KG.ingest.list-durable-media. A recipe's image is stored as a
content-addressed **blob** with a ``:MediaAsset`` graph node (carrying the recipe id +
slug), in ONE cross-modal ACID commit, via the agent-utilities ``MediaStore`` obtained
through the shared ``native_ingest.media_store`` primitive. This makes the raw image
bytes — not just a URL — durable, deduped and queryable inside the knowledge graph.

Entirely best-effort and dependency-/engine-guarded: with no KG stack or no reachable
engine every entry point **no-ops** (returns ``None``), so the connector keeps working
with zero KG infrastructure. Mealie serves recipe images at
``/api/media/recipes/{recipe_id}/images/{file_name}``.
"""

from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urljoin

logger = logging.getLogger("mealie_mcp.kg.media")

_SOURCE = "mealie-mcp"


def media_store() -> Any | None:
    """Return a ``MediaStore`` over a live engine, or ``None`` when unavailable."""
    try:
        from agent_utilities.knowledge_graph.memory.native_ingest import (
            media_store as _shared_media_store,
        )

        store = _shared_media_store()
        if store is not None:
            return store
    except Exception as e:  # noqa: BLE001 — shared primitive absent, fall back
        logger.debug("mealie KG media: shared primitive unavailable: %s", e)
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
        from agent_utilities.knowledge_graph.memory.media_store import MediaStore
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("mealie KG media unavailable (import): %s", e)
        return None
    try:
        engine = GraphComputeEngine()
        if getattr(engine, "_client", None) is None:
            return None
        return MediaStore(engine)
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("mealie KG media: engine unreachable: %s", e)
        return None


def fetch_recipe_image_bytes(
    client: Any, recipe_id: str, file_name: str = "original.webp"
) -> bytes | None:
    """Fetch the raw image bytes for a recipe via the client's HTTP session.

    The typed ``client.request`` decodes JSON/text, so raw image bytes are pulled
    straight from the underlying ``requests`` session. Returns ``None`` on any error.
    """
    try:
        base_url = getattr(client, "base_url", "") or ""
        session = getattr(client, "_session", None)
        if session is None:
            return None
        url = urljoin(base_url, f"/api/media/recipes/{recipe_id}/images/{file_name}")
        resp = session.get(url, proxies=getattr(client, "proxies", None))
        if resp.status_code >= 400:
            logger.debug("mealie KG media: image fetch %s -> %s", url, resp.status_code)
            return None
        return resp.content
    except Exception as e:  # noqa: BLE001 — network/attr error is non-fatal
        logger.debug("mealie KG media: image fetch failed: %s", e)
        return None


def ingest_recipe_image(
    recipe: dict[str, Any],
    *,
    image_bytes: bytes,
    mime_type: str = "image/webp",
    source: str = _SOURCE,
    store: Any | None = None,
) -> dict[str, Any] | None:
    """Store a recipe image as a blob + ``:MediaAsset`` in the knowledge graph.

    Returns ``{asset_id, digest, size_bytes, recipe_node_id}`` on success, or ``None``
    when there is no engine, no bytes, or the store failed (never raises). ``store``
    may be injected (tests); otherwise one is built on demand.
    """
    if not image_bytes:
        return None
    rid = recipe.get("id")
    if rid is None:
        return None
    rid = str(rid)
    store = store if store is not None else media_store()
    if store is None:
        return None

    recipe_node_id = f"mealie:recipe:{rid}"
    name = recipe.get("name") or recipe.get("slug") or rid
    extra = {
        "recipe_id": rid,
        "recipe_node_id": recipe_node_id,
        "slug": recipe.get("slug"),
        "recipe_name": recipe.get("name"),
    }
    extra = {k: v for k, v in extra.items() if v is not None}

    try:
        stored = store.store_media(
            image_bytes,
            media_type="image",
            mime_type=mime_type,
            source=source,
            name=name,
            extra=extra,
        )
    except Exception as e:  # noqa: BLE001 — engine/store failure is non-fatal
        logger.warning("mealie KG media: store_media failed: %s", e)
        return None
    if stored is None:
        return None

    asset_id = getattr(stored, "asset_id", None)
    digest = getattr(stored, "digest", None)
    logger.info(
        "mealie KG media: stored image for recipe %s (%d bytes) as asset %s",
        rid,
        len(image_bytes),
        asset_id,
    )
    return {
        "asset_id": asset_id,
        "digest": digest,
        "size_bytes": len(image_bytes),
        "recipe_node_id": recipe_node_id,
    }
