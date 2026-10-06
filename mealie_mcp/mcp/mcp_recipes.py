"""MCP tools for recipes operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from mealie_mcp.auth import get_client
from mealie_mcp.recipe_tools import (
    add_recipe_write_tools as _add_recipe_write_tools,
)

VALID_RECIPES_ACTIONS = (
    "get_recipe_formats_and_templates",
    "get_recipe_as_format",
    "test_parse_recipe_url",
    "create_recipe_from_html_or_json",
    "parse_recipe_url",
    "parse_recipe_url_bulk",
    "create_recipe_from_zip",
    "create_recipe_from_image",
    "get_recipes",
    "post_recipes",
    "put_recipes",
    "patch_many",
    "get_recipes_suggestions",
    "get_recipes_slug",
    "put_recipes_slug",
    "patch_one",
    "delete_recipes_slug",
    "duplicate_one",
    "update_last_made",
    "scrape_image_url",
    "update_recipe_image",
    "delete_recipe_image",
    "upload_recipe_asset",
    "get_recipe_comments",
    "bulk_tag_recipes",
    "bulk_settings_recipes",
    "bulk_categorize_recipes",
    "bulk_delete_recipes",
    "bulk_export_recipes",
    "get_exported_data",
    "get_exported_data_token",
    "purge_export_data",
    "get_shared_recipe",
    "get_shared_recipe_as_zip",
    "get_recipes_timeline_events",
    "post_recipes_timeline_events",
    "get_recipes_timeline_events_item_id",
    "put_recipes_timeline_events_item_id",
    "delete_recipes_timeline_events_item_id",
    "update_event_image",
    "get_comments",
    "post_comments",
    "get_comments_item_id",
    "put_comments_item_id",
    "post_parser_ingredient",
    "parse_ingredient",
    "parse_ingredients",
    "get_foods",
    "post_foods",
    "put_foods_merge",
    "get_foods_item_id",
    "put_foods_item_id",
    "delete_foods_item_id",
    "get_units",
    "post_units",
    "put_units_merge",
    "get_units_item_id",
    "put_units_item_id",
    "delete_units_item_id",
    "get_recipe_img",
    "get_recipe_timeline_event_img",
    "get_recipe_asset",
    "get_user_image",
    "get_validation_text",
)


async def _recipes_get_recipe_formats_and_templates(client, **kwargs):
    return await run_blocking(client.get_recipe_formats_and_templates, **kwargs)


async def _recipes_get_recipe_as_format(client, **kwargs):
    return await run_blocking(client.get_recipe_as_format, **kwargs)


async def _recipes_test_parse_recipe_url(client, **kwargs):
    return await run_blocking(client.test_parse_recipe_url, **kwargs)


async def _recipes_create_recipe_from_html_or_json(client, **kwargs):
    return await run_blocking(client.create_recipe_from_html_or_json, **kwargs)


async def _recipes_parse_recipe_url(client, **kwargs):
    return await run_blocking(client.parse_recipe_url, **kwargs)


async def _recipes_parse_recipe_url_bulk(client, **kwargs):
    return await run_blocking(client.parse_recipe_url_bulk, **kwargs)


async def _recipes_create_recipe_from_zip(client, **kwargs):
    return await run_blocking(client.create_recipe_from_zip, **kwargs)


async def _recipes_create_recipe_from_image(client, **kwargs):
    return await run_blocking(client.create_recipe_from_image, **kwargs)


async def _recipes_get_recipes(client, **kwargs):
    return await run_blocking(client.get_recipes, **kwargs)


async def _recipes_post_recipes(client, **kwargs):
    return await run_blocking(client.post_recipes, **kwargs)


async def _recipes_put_recipes(client, **kwargs):
    return await run_blocking(client.put_recipes, **kwargs)


async def _recipes_patch_many(client, **kwargs):
    return await run_blocking(client.patch_many, **kwargs)


async def _recipes_get_recipes_suggestions(client, **kwargs):
    return await run_blocking(client.get_recipes_suggestions, **kwargs)


async def _recipes_get_recipes_slug(client, **kwargs):
    return await run_blocking(client.get_recipes_slug, **kwargs)


async def _recipes_put_recipes_slug(client, **kwargs):
    return await run_blocking(client.put_recipes_slug, **kwargs)


async def _recipes_patch_one(client, **kwargs):
    return await run_blocking(client.patch_one, **kwargs)


async def _recipes_delete_recipes_slug(client, **kwargs):
    return await run_blocking(client.delete_recipes_slug, **kwargs)


async def _recipes_duplicate_one(client, **kwargs):
    return await run_blocking(client.duplicate_one, **kwargs)


async def _recipes_update_last_made(client, **kwargs):
    return await run_blocking(client.update_last_made, **kwargs)


async def _recipes_scrape_image_url(client, **kwargs):
    return await run_blocking(client.scrape_image_url, **kwargs)


async def _recipes_update_recipe_image(client, **kwargs):
    return await run_blocking(client.update_recipe_image, **kwargs)


async def _recipes_delete_recipe_image(client, **kwargs):
    return await run_blocking(client.delete_recipe_image, **kwargs)


async def _recipes_upload_recipe_asset(client, **kwargs):
    return await run_blocking(client.upload_recipe_asset, **kwargs)


async def _recipes_get_recipe_comments(client, **kwargs):
    return await run_blocking(client.get_recipe_comments, **kwargs)


async def _recipes_bulk_tag_recipes(client, **kwargs):
    return await run_blocking(client.bulk_tag_recipes, **kwargs)


async def _recipes_bulk_settings_recipes(client, **kwargs):
    return await run_blocking(client.bulk_settings_recipes, **kwargs)


async def _recipes_bulk_categorize_recipes(client, **kwargs):
    return await run_blocking(client.bulk_categorize_recipes, **kwargs)


async def _recipes_bulk_delete_recipes(client, **kwargs):
    return await run_blocking(client.bulk_delete_recipes, **kwargs)


async def _recipes_bulk_export_recipes(client, **kwargs):
    return await run_blocking(client.bulk_export_recipes, **kwargs)


async def _recipes_get_exported_data(client, **kwargs):
    return await run_blocking(client.get_exported_data, **kwargs)


async def _recipes_get_exported_data_token(client, **kwargs):
    return await run_blocking(client.get_exported_data_token, **kwargs)


async def _recipes_purge_export_data(client, **kwargs):
    return await run_blocking(client.purge_export_data, **kwargs)


async def _recipes_get_shared_recipe(client, **kwargs):
    return await run_blocking(client.get_shared_recipe, **kwargs)


async def _recipes_get_shared_recipe_as_zip(client, **kwargs):
    return await run_blocking(client.get_shared_recipe_as_zip, **kwargs)


async def _recipes_get_recipes_timeline_events(client, **kwargs):
    return await run_blocking(client.get_recipes_timeline_events, **kwargs)


async def _recipes_post_recipes_timeline_events(client, **kwargs):
    return await run_blocking(client.post_recipes_timeline_events, **kwargs)


async def _recipes_get_recipes_timeline_events_item_id(client, **kwargs):
    return await run_blocking(client.get_recipes_timeline_events_item_id, **kwargs)


async def _recipes_put_recipes_timeline_events_item_id(client, **kwargs):
    return await run_blocking(client.put_recipes_timeline_events_item_id, **kwargs)


async def _recipes_delete_recipes_timeline_events_item_id(client, **kwargs):
    return await run_blocking(client.delete_recipes_timeline_events_item_id, **kwargs)


async def _recipes_update_event_image(client, **kwargs):
    return await run_blocking(client.update_event_image, **kwargs)


async def _recipes_get_comments(client, **kwargs):
    return await run_blocking(client.get_comments, **kwargs)


async def _recipes_post_comments(client, **kwargs):
    return await run_blocking(client.post_comments, **kwargs)


async def _recipes_get_comments_item_id(client, **kwargs):
    return await run_blocking(client.get_comments_item_id, **kwargs)


async def _recipes_put_comments_item_id(client, **kwargs):
    return await run_blocking(client.put_comments_item_id, **kwargs)


async def _recipes_post_parser_ingredient(client, **kwargs):
    return await run_blocking(client.post_parser_ingredient, **kwargs)


async def _recipes_parse_ingredient(client, **kwargs):
    return await run_blocking(client.parse_ingredient, **kwargs)


async def _recipes_parse_ingredients(client, **kwargs):
    return await run_blocking(client.parse_ingredients, **kwargs)


async def _recipes_get_foods(client, **kwargs):
    return await run_blocking(client.get_foods, **kwargs)


async def _recipes_post_foods(client, **kwargs):
    return await run_blocking(client.post_foods, **kwargs)


async def _recipes_put_foods_merge(client, **kwargs):
    return await run_blocking(client.put_foods_merge, **kwargs)


async def _recipes_get_foods_item_id(client, **kwargs):
    return await run_blocking(client.get_foods_item_id, **kwargs)


async def _recipes_put_foods_item_id(client, **kwargs):
    return await run_blocking(client.put_foods_item_id, **kwargs)


async def _recipes_delete_foods_item_id(client, **kwargs):
    return await run_blocking(client.delete_foods_item_id, **kwargs)


async def _recipes_get_units(client, **kwargs):
    return await run_blocking(client.get_units, **kwargs)


async def _recipes_post_units(client, **kwargs):
    return await run_blocking(client.post_units, **kwargs)


async def _recipes_put_units_merge(client, **kwargs):
    return await run_blocking(client.put_units_merge, **kwargs)


async def _recipes_get_units_item_id(client, **kwargs):
    return await run_blocking(client.get_units_item_id, **kwargs)


async def _recipes_put_units_item_id(client, **kwargs):
    return await run_blocking(client.put_units_item_id, **kwargs)


async def _recipes_delete_units_item_id(client, **kwargs):
    return await run_blocking(client.delete_units_item_id, **kwargs)


async def _recipes_get_recipe_img(client, **kwargs):
    return await run_blocking(client.get_recipe_img, **kwargs)


async def _recipes_get_recipe_timeline_event_img(client, **kwargs):
    return await run_blocking(client.get_recipe_timeline_event_img, **kwargs)


async def _recipes_get_recipe_asset(client, **kwargs):
    return await run_blocking(client.get_recipe_asset, **kwargs)


async def _recipes_get_user_image(client, **kwargs):
    return await run_blocking(client.get_user_image, **kwargs)


async def _recipes_get_validation_text(client, **kwargs):
    return await run_blocking(client.get_validation_text, **kwargs)


_RECIPES_ACTION_HANDLERS = {
    "get_recipe_formats_and_templates": _recipes_get_recipe_formats_and_templates,
    "get_recipe_as_format": _recipes_get_recipe_as_format,
    "test_parse_recipe_url": _recipes_test_parse_recipe_url,
    "create_recipe_from_html_or_json": _recipes_create_recipe_from_html_or_json,
    "parse_recipe_url": _recipes_parse_recipe_url,
    "parse_recipe_url_bulk": _recipes_parse_recipe_url_bulk,
    "create_recipe_from_zip": _recipes_create_recipe_from_zip,
    "create_recipe_from_image": _recipes_create_recipe_from_image,
    "get_recipes": _recipes_get_recipes,
    "post_recipes": _recipes_post_recipes,
    "put_recipes": _recipes_put_recipes,
    "patch_many": _recipes_patch_many,
    "get_recipes_suggestions": _recipes_get_recipes_suggestions,
    "get_recipes_slug": _recipes_get_recipes_slug,
    "put_recipes_slug": _recipes_put_recipes_slug,
    "patch_one": _recipes_patch_one,
    "delete_recipes_slug": _recipes_delete_recipes_slug,
    "duplicate_one": _recipes_duplicate_one,
    "update_last_made": _recipes_update_last_made,
    "scrape_image_url": _recipes_scrape_image_url,
    "update_recipe_image": _recipes_update_recipe_image,
    "delete_recipe_image": _recipes_delete_recipe_image,
    "upload_recipe_asset": _recipes_upload_recipe_asset,
    "get_recipe_comments": _recipes_get_recipe_comments,
    "bulk_tag_recipes": _recipes_bulk_tag_recipes,
    "bulk_settings_recipes": _recipes_bulk_settings_recipes,
    "bulk_categorize_recipes": _recipes_bulk_categorize_recipes,
    "bulk_delete_recipes": _recipes_bulk_delete_recipes,
    "bulk_export_recipes": _recipes_bulk_export_recipes,
    "get_exported_data": _recipes_get_exported_data,
    "get_exported_data_token": _recipes_get_exported_data_token,
    "purge_export_data": _recipes_purge_export_data,
    "get_shared_recipe": _recipes_get_shared_recipe,
    "get_shared_recipe_as_zip": _recipes_get_shared_recipe_as_zip,
    "get_recipes_timeline_events": _recipes_get_recipes_timeline_events,
    "post_recipes_timeline_events": _recipes_post_recipes_timeline_events,
    "get_recipes_timeline_events_item_id": _recipes_get_recipes_timeline_events_item_id,
    "put_recipes_timeline_events_item_id": _recipes_put_recipes_timeline_events_item_id,
    "delete_recipes_timeline_events_item_id": _recipes_delete_recipes_timeline_events_item_id,
    "update_event_image": _recipes_update_event_image,
    "get_comments": _recipes_get_comments,
    "post_comments": _recipes_post_comments,
    "get_comments_item_id": _recipes_get_comments_item_id,
    "put_comments_item_id": _recipes_put_comments_item_id,
    "post_parser_ingredient": _recipes_post_parser_ingredient,
    "parse_ingredient": _recipes_parse_ingredient,
    "parse_ingredients": _recipes_parse_ingredients,
    "get_foods": _recipes_get_foods,
    "post_foods": _recipes_post_foods,
    "put_foods_merge": _recipes_put_foods_merge,
    "get_foods_item_id": _recipes_get_foods_item_id,
    "put_foods_item_id": _recipes_put_foods_item_id,
    "delete_foods_item_id": _recipes_delete_foods_item_id,
    "get_units": _recipes_get_units,
    "post_units": _recipes_post_units,
    "put_units_merge": _recipes_put_units_merge,
    "get_units_item_id": _recipes_get_units_item_id,
    "put_units_item_id": _recipes_put_units_item_id,
    "delete_units_item_id": _recipes_delete_units_item_id,
    "get_recipe_img": _recipes_get_recipe_img,
    "get_recipe_timeline_event_img": _recipes_get_recipe_timeline_event_img,
    "get_recipe_asset": _recipes_get_recipe_asset,
    "get_user_image": _recipes_get_user_image,
    "get_validation_text": _recipes_get_validation_text,
}


def register_recipes_tools(mcp: FastMCP):
    _add_recipe_write_tools(mcp)

    @mcp.tool(tags={"recipes"})
    async def mealie_recipes(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_recipe_formats_and_templates', 'get_recipe_as_format', 'test_parse_recipe_url', 'create_recipe_from_html_or_json', 'parse_recipe_url', 'parse_recipe_url_bulk', 'create_recipe_from_zip', 'create_recipe_from_image', 'get_recipes', 'post_recipes', 'put_recipes', 'patch_many', 'get_recipes_suggestions', 'get_recipes_slug', 'put_recipes_slug', 'patch_one', 'delete_recipes_slug', 'duplicate_one', 'update_last_made', 'scrape_image_url', 'update_recipe_image', 'delete_recipe_image', 'upload_recipe_asset', 'get_recipe_comments', 'bulk_tag_recipes', 'bulk_settings_recipes', 'bulk_categorize_recipes', 'bulk_delete_recipes', 'bulk_export_recipes', 'get_exported_data', 'get_exported_data_token', 'purge_export_data', 'get_shared_recipe', 'get_shared_recipe_as_zip', 'get_recipes_timeline_events', 'post_recipes_timeline_events', 'get_recipes_timeline_events_item_id', 'put_recipes_timeline_events_item_id', 'delete_recipes_timeline_events_item_id', 'update_event_image', 'get_comments', 'post_comments', 'get_comments_item_id', 'put_comments_item_id', 'post_parser_ingredient', 'parse_ingredient', 'parse_ingredients', 'get_foods', 'post_foods', 'put_foods_merge', 'get_foods_item_id', 'put_foods_item_id', 'delete_foods_item_id', 'get_units', 'post_units', 'put_units_merge', 'get_units_item_id', 'put_units_item_id', 'delete_units_item_id', 'get_recipe_img', 'get_recipe_timeline_event_img', 'get_recipe_asset', 'get_user_image', 'get_validation_text'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage mealie recipes operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, VALID_RECIPES_ACTIONS, service="mealie-mcp")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        handler = _RECIPES_ACTION_HANDLERS.get(action)
        if handler is None:
            raise ValueError(f"Unknown action: {action}")
        return await handler(client, **kwargs)
