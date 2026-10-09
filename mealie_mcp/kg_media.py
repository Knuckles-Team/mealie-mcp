"""Native epistemic-graph blob ingestion for Mealie recipe images.

CONCEPT:AU-KG.ingest.list-durable-media. A recipe's image is stored as a
content-addressed **blob** with an ``:AssetOccurrence`` graph node (carrying the
recipe id + slug), in ONE cross-modal ACID commit, via the
``agent_connector_sdk.ingest`` knowledge-ingest facade's ``MediaAsset`` on a
``ChangeSet``. This makes the raw image bytes — not just a URL — durable,
deduped and queryable inside the knowledge graph.

Entirely best-effort and engine-guarded: with no reachable engine every entry
point **no-ops** (returns ``None``), so the connector keeps working with zero
KG infrastructure. Mealie serves recipe images at
``/api/media/recipes/{recipe_id}/images/{file_name}``.
"""

from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urljoin

from agent_connector_sdk.ingest import (
    ChangeSet,
    EntityRef,
    IngestBinding,
    IngestError,
    KnowledgeIngest,
    MediaAsset,
    Relationship,
    current_ingest,
)

logger = logging.getLogger("mealie_mcp.kg.media")

_SOURCE = "mealie-mcp"
_BINDING = IngestBinding(connector="mealie-mcp", stream="mealie", media_type="AssetOccurrence")


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
        resp = session.get(url)
        if resp.status_code >= 400:
            logger.debug(
                "Mealie KG media fetch failed: status_code=%s", resp.status_code
            )
            return None
        return resp.content
    except Exception as e:  # noqa: BLE001 — network/attr error is non-fatal
        logger.debug("Mealie KG media fetch failed: error_type=%s", type(e).__name__)
        return None


async def ingest_recipe_image(
    recipe: dict[str, Any],
    *,
    image_bytes: bytes,
    mime_type: str = "image/webp",
    source: str = _SOURCE,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, Any] | None:
    """Store a recipe image as a blob + ``:AssetOccurrence`` in the knowledge graph.

    Returns ``{asset_id, size_bytes, recipe_node_id}`` on success, or ``None``
    when there is no engine, no bytes, or the commit failed (never raises).
    ``ingest`` may be injected (tests) with a fake transport; otherwise the
    process-global service is used.
    """
    if not image_bytes:
        return None
    rid = recipe.get("id")
    if rid is None:
        return None
    rid = str(rid)

    recipe_node_id = f"mealie:recipe:{rid}"
    asset_id = f"mealie:asset:{rid}"
    name = recipe.get("name") or recipe.get("slug") or rid
    properties = {
        "recipe_id": rid,
        "recipe_node_id": recipe_node_id,
        "slug": recipe.get("slug"),
        "recipe_name": recipe.get("name"),
        "source": source,
    }
    properties = {k: v for k, v in properties.items() if v is not None}

    asset = MediaAsset(
        data=image_bytes,
        mime_type=mime_type,
        id=asset_id,
        name=str(name),
        properties=properties,
    )
    relationship = Relationship(
        source=EntityRef(id=recipe_node_id, node_type="Recipe"),
        target=asset_id,
        relationship="hasImage",
    )
    change_set = ChangeSet(media=(asset,), relationships=(relationship,))

    try:
        service = ingest or current_ingest()
        await service.submit(_BINDING, change_set)
    except IngestError as e:  # noqa: BLE001 — engine unreachable is non-fatal
        logger.warning("Mealie KG media store failed: error_type=%s", type(e).__name__)
        return None

    logger.info(
        "mealie KG media: stored image for recipe %s (%d bytes) as asset %s",
        rid,
        len(image_bytes),
        asset_id,
    )
    return {
        "asset_id": asset_id,
        "size_bytes": len(image_bytes),
        "recipe_node_id": recipe_node_id,
    }
