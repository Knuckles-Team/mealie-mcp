#!/usr/bin/python
import warnings

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field
from scion_sdk.mcp.concurrency import run_blocking

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")


from mealie_mcp.auth import get_client
from mealie_mcp.recipe_tools import add_recipe_write_tools


def register_recipes_tools(mcp: FastMCP):
    """Register the typed recipe write tools."""
    add_recipe_write_tools(mcp)


def register_kg_tools(mcp: FastMCP):
    @mcp.tool(tags={"kg"})
    async def mealie_ingest_recipes(
        params_json: str = Field(
            default="{}",
            description='JSON string of get_recipes filters (e.g. {"per_page": 100, "categories": "Dinner"}).',
        ),
        ingest_images: bool = Field(
            default=False,
            description="Also fetch each recipe image and store it as a :AssetOccurrence blob.",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Natively ingest Mealie recipes into epistemic-graph as typed :Recipe nodes.

        Lists recipes via the Mealie API and pushes them (with their :Ingredient,
        :Food, :Unit, :RecipeCategory, :Tag and :RecipeTool nodes + links) into the
        knowledge graph via the fast engine client. With ``ingest_images`` the raw
        image bytes are stored as content-addressed :AssetOccurrence blobs. Best-effort:
        returns ``{"ingested": None}`` when no engine is reachable.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        import json as _json

        from mealie_mcp.kg_ingest import ingest_recipes
        from mealie_mcp.kg_media import fetch_recipe_image_bytes, ingest_recipe_image

        if ctx:
            await ctx.info("Listing recipes for KG ingestion...")
        try:
            kwargs = _json.loads(params_json) if params_json else {}
        except Exception:  # noqa: BLE001
            return {"error": "Operation failed"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resp = await run_blocking(client.get_recipes, **kwargs)
        data = resp.get("items", resp) if isinstance(resp, dict) else resp
        records = data if isinstance(data, list) else [data]
        recipes = [r for r in records if isinstance(r, dict) and r.get("id")]

        result = await ingest_recipes(recipes)

        images = 0
        if ingest_images:
            for recipe in recipes:
                image_bytes = await run_blocking(
                    fetch_recipe_image_bytes, client, str(recipe["id"])
                )
                if not image_bytes:
                    continue
                if (
                    await ingest_recipe_image(recipe, image_bytes=image_bytes)
                    is not None
                ):
                    images += 1

        return {"listed": len(recipes), "ingested": result, "images_ingested": images}

    return None
