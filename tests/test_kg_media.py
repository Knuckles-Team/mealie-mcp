"""Native epistemic-graph media ingestion — Wire-First live-path coverage.

Exercises the real ``ingest_recipe_image`` / ``fetch_recipe_image_bytes`` seam with a
fake ``MediaStore`` and a fake HTTP session (no engine required).
CONCEPT:AU-KG.ingest.list-durable-media.
"""

from __future__ import annotations

from dataclasses import dataclass

from mealie_mcp.kg_media import fetch_recipe_image_bytes, ingest_recipe_image


@dataclass
class _Stored:
    asset_id: str
    digest: str


class _FakeMediaStore:
    def __init__(self):
        self.calls = []

    def store_media(self, data, **kw):
        self.calls.append((data, kw))
        return _Stored(asset_id="media:cafef00d", digest="cafef00d")


def test_ingest_recipe_image_stores_bytes_and_metadata():
    store = _FakeMediaStore()
    recipe = {"id": "r-1", "name": "Carbonara", "slug": "carbonara"}
    res = ingest_recipe_image(recipe, image_bytes=b"\x00webp-bytes", store=store)

    assert res is not None
    assert res["asset_id"] == "media:cafef00d"
    assert res["digest"] == "cafef00d"
    assert res["size_bytes"] == len(b"\x00webp-bytes")
    assert res["recipe_node_id"] == "mealie:recipe:r-1"

    assert len(store.calls) == 1
    data, kw = store.calls[0]
    assert data == b"\x00webp-bytes"
    assert kw["source"] == "mealie-mcp"
    assert kw["media_type"] == "image"
    assert kw["mime_type"] == "image/webp"
    assert kw["name"] == "Carbonara"
    assert kw["extra"]["recipe_id"] == "r-1"
    assert kw["extra"]["recipe_node_id"] == "mealie:recipe:r-1"


def test_ingest_recipe_image_noops_without_engine():
    # No injected store + no reachable engine -> clean no-op (never raises).
    assert ingest_recipe_image({"id": "r-1"}, image_bytes=b"x") is None


def test_ingest_recipe_image_noops_on_empty_bytes():
    assert (
        ingest_recipe_image({"id": "r-1"}, image_bytes=b"", store=_FakeMediaStore())
        is None
    )


def test_ingest_recipe_image_noops_without_id():
    assert (
        ingest_recipe_image({"name": "x"}, image_bytes=b"x", store=_FakeMediaStore())
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
