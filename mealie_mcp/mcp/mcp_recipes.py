"""MCP tools for recipes operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from mealie_mcp.auth import get_client


def register_recipes_tools(mcp: FastMCP):
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
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_recipe_formats_and_templates":
            return client.get_recipe_formats_and_templates(**kwargs)
        if action == "get_recipe_as_format":
            return client.get_recipe_as_format(**kwargs)
        if action == "test_parse_recipe_url":
            return client.test_parse_recipe_url(**kwargs)
        if action == "create_recipe_from_html_or_json":
            return client.create_recipe_from_html_or_json(**kwargs)
        if action == "parse_recipe_url":
            return client.parse_recipe_url(**kwargs)
        if action == "parse_recipe_url_bulk":
            return client.parse_recipe_url_bulk(**kwargs)
        if action == "create_recipe_from_zip":
            return client.create_recipe_from_zip(**kwargs)
        if action == "create_recipe_from_image":
            return client.create_recipe_from_image(**kwargs)
        if action == "get_recipes":
            return client.get_recipes(**kwargs)
        if action == "post_recipes":
            return client.post_recipes(**kwargs)
        if action == "put_recipes":
            return client.put_recipes(**kwargs)
        if action == "patch_many":
            return client.patch_many(**kwargs)
        if action == "get_recipes_suggestions":
            return client.get_recipes_suggestions(**kwargs)
        if action == "get_recipes_slug":
            return client.get_recipes_slug(**kwargs)
        if action == "put_recipes_slug":
            return client.put_recipes_slug(**kwargs)
        if action == "patch_one":
            return client.patch_one(**kwargs)
        if action == "delete_recipes_slug":
            return client.delete_recipes_slug(**kwargs)
        if action == "duplicate_one":
            return client.duplicate_one(**kwargs)
        if action == "update_last_made":
            return client.update_last_made(**kwargs)
        if action == "scrape_image_url":
            return client.scrape_image_url(**kwargs)
        if action == "update_recipe_image":
            return client.update_recipe_image(**kwargs)
        if action == "delete_recipe_image":
            return client.delete_recipe_image(**kwargs)
        if action == "upload_recipe_asset":
            return client.upload_recipe_asset(**kwargs)
        if action == "get_recipe_comments":
            return client.get_recipe_comments(**kwargs)
        if action == "bulk_tag_recipes":
            return client.bulk_tag_recipes(**kwargs)
        if action == "bulk_settings_recipes":
            return client.bulk_settings_recipes(**kwargs)
        if action == "bulk_categorize_recipes":
            return client.bulk_categorize_recipes(**kwargs)
        if action == "bulk_delete_recipes":
            return client.bulk_delete_recipes(**kwargs)
        if action == "bulk_export_recipes":
            return client.bulk_export_recipes(**kwargs)
        if action == "get_exported_data":
            return client.get_exported_data(**kwargs)
        if action == "get_exported_data_token":
            return client.get_exported_data_token(**kwargs)
        if action == "purge_export_data":
            return client.purge_export_data(**kwargs)
        if action == "get_shared_recipe":
            return client.get_shared_recipe(**kwargs)
        if action == "get_shared_recipe_as_zip":
            return client.get_shared_recipe_as_zip(**kwargs)
        if action == "get_recipes_timeline_events":
            return client.get_recipes_timeline_events(**kwargs)
        if action == "post_recipes_timeline_events":
            return client.post_recipes_timeline_events(**kwargs)
        if action == "get_recipes_timeline_events_item_id":
            return client.get_recipes_timeline_events_item_id(**kwargs)
        if action == "put_recipes_timeline_events_item_id":
            return client.put_recipes_timeline_events_item_id(**kwargs)
        if action == "delete_recipes_timeline_events_item_id":
            return client.delete_recipes_timeline_events_item_id(**kwargs)
        if action == "update_event_image":
            return client.update_event_image(**kwargs)
        if action == "get_comments":
            return client.get_comments(**kwargs)
        if action == "post_comments":
            return client.post_comments(**kwargs)
        if action == "get_comments_item_id":
            return client.get_comments_item_id(**kwargs)
        if action == "put_comments_item_id":
            return client.put_comments_item_id(**kwargs)
        if action == "post_parser_ingredient":
            return client.post_parser_ingredient(**kwargs)
        if action == "parse_ingredient":
            return client.parse_ingredient(**kwargs)
        if action == "parse_ingredients":
            return client.parse_ingredients(**kwargs)
        if action == "get_foods":
            return client.get_foods(**kwargs)
        if action == "post_foods":
            return client.post_foods(**kwargs)
        if action == "put_foods_merge":
            return client.put_foods_merge(**kwargs)
        if action == "get_foods_item_id":
            return client.get_foods_item_id(**kwargs)
        if action == "put_foods_item_id":
            return client.put_foods_item_id(**kwargs)
        if action == "delete_foods_item_id":
            return client.delete_foods_item_id(**kwargs)
        if action == "get_units":
            return client.get_units(**kwargs)
        if action == "post_units":
            return client.post_units(**kwargs)
        if action == "put_units_merge":
            return client.put_units_merge(**kwargs)
        if action == "get_units_item_id":
            return client.get_units_item_id(**kwargs)
        if action == "put_units_item_id":
            return client.put_units_item_id(**kwargs)
        if action == "delete_units_item_id":
            return client.delete_units_item_id(**kwargs)
        if action == "get_recipe_img":
            return client.get_recipe_img(**kwargs)
        if action == "get_recipe_timeline_event_img":
            return client.get_recipe_timeline_event_img(**kwargs)
        if action == "get_recipe_asset":
            return client.get_recipe_asset(**kwargs)
        if action == "get_user_image":
            return client.get_user_image(**kwargs)
        if action == "get_validation_text":
            return client.get_validation_text(**kwargs)
        raise ValueError(f"Unknown action: {action}")
