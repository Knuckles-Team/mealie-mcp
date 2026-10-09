"""Native epistemic-graph media ingestion — Wire-First live-path coverage.

Exercises the real ``ingest_recipe_image`` / ``fetch_recipe_image_bytes`` seam with
a fake transport one level below ``agent_connector_sdk.ingest.KnowledgeIngest``
and a fake HTTP session (no engine required).
CONCEPT:AU-KG.ingest.list-durable-media.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import KnowledgeIngest

from mealie_mcp.kg_media import fetch_recipe_image_bytes, ingest_recipe_image


class _FakeTransport:
    def __init__(self) -> None:
        self.requests: list[Any] = []
        self.blobs: list[bytes] = []

    async def source_status(self, connector: str, stream: str):
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request):
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data: bytes) -> str:
        self.blobs.append(data)
        return "cafef00d"


@pytest.fixture
def ingest():
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


async def test_ingest_recipe_image_stores_bytes_and_metadata(ingest):
    service, transport = ingest
    recipe = {"id": "r-1", "name": "Carbonara", "slug": "carbonara"}
    res = await ingest_recipe_image(
        recipe, image_bytes=b"\x00webp-bytes", ingest=service
    )

    assert res is not None
    assert res["asset_id"] == "mealie:asset:r-1"
    assert res["size_bytes"] == len(b"\x00webp-bytes")
    assert res["recipe_node_id"] == "mealie:recipe:r-1"

    assert transport.blobs == [b"\x00webp-bytes"]
    request = transport.requests[0]
    by_id = {record.record_id: record for record in request.records}
    asset_record = by_id["mealie:asset:r-1"]
    assert asset_record.payload["mime_type"] == "image/webp"
    assert asset_record.payload["name"] == "Carbonara"
    edge_types = {
        (rel.source.record_id, rel.target.record_id, rel.relation_reference.rsplit("/relations/", 1)[-1])
        for rel in request.relationships
    }
    assert ("mealie:recipe:r-1", "mealie:asset:r-1", "hasImage") in edge_types


async def test_ingest_recipe_image_noops_without_engine():
    # No injected service + no reachable engine -> clean no-op (never raises).
    assert await ingest_recipe_image({"id": "r-1"}, image_bytes=b"x") is None


async def test_ingest_recipe_image_noops_on_empty_bytes(ingest):
    service, _ = ingest
    assert (
        await ingest_recipe_image({"id": "r-1"}, image_bytes=b"", ingest=service)
        is None
    )


async def test_ingest_recipe_image_noops_without_id(ingest):
    service, _ = ingest
    assert (
        await ingest_recipe_image({"name": "x"}, image_bytes=b"x", ingest=service)
        is None
    )


class _FakeResp:
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content


class _FakeSession:
    def __init__(self, resp):
        self._resp = resp
        self.calls = []

    def get(self, url, **kw):
        self.calls.append(url)
        return self._resp


class _FakeApiClient:
    def __init__(self, resp):
        self.base_url = "https://mealie.test"
        self._session = _FakeSession(resp)
        self.proxies = None


def test_fetch_recipe_image_bytes_ok():
    client = _FakeApiClient(_FakeResp(200, b"IMGDATA"))
    data = fetch_recipe_image_bytes(client, "r-1")
    assert data == b"IMGDATA"
    assert client._session.calls == [
        "https://mealie.test/api/media/recipes/r-1/images/original.webp"
    ]


def test_fetch_recipe_image_bytes_error_is_none():
    client = _FakeApiClient(_FakeResp(404, b""))
    assert fetch_recipe_image_bytes(client, "r-1") is None
