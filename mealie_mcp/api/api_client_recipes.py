#!/usr/bin/env python
from typing import Any

from mealie_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def get_recipe_formats_and_templates(
        self, accept_language: Any | None = None
    ) -> Any:
        """Get Recipe Formats And Templates"""
        params = None
        return self.request("GET", "/api/recipes/exports", params=params, data=None)

    def get_recipe_as_format(
        self, slug: str, template_name: str, accept_language: Any | None = None
    ) -> Any:
        """Get Recipe As Format"""
        params: dict[str, Any] = {}
        if template_name is not None:
            params["template_name"] = template_name
        return self.request(
            "GET", f"/api/recipes/{slug}/exports", params=params, data=None
        )

    def test_parse_recipe_url(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Test Parse Recipe Url"""
        params = None
        return self.request(
            "POST", "/api/recipes/test-scrape-url", params=params, data=data
        )

    def create_recipe_from_html_or_json(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create Recipe From Html Or Json"""
        params = None
        return self.request(
            "POST", "/api/recipes/create/html-or-json", params=params, data=data
        )

    def parse_recipe_url(self, data: dict, accept_language: Any | None = None) -> Any:
        """Parse Recipe Url"""
        params = None
        return self.request("POST", "/api/recipes/create/url", params=params, data=data)

    def parse_recipe_url_bulk(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Parse Recipe Url Bulk"""
        params = None
        return self.request(
            "POST", "/api/recipes/create/url/bulk", params=params, data=data
        )

    def create_recipe_from_zip(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create Recipe From Zip"""
        params = None
        return self.request("POST", "/api/recipes/create/zip", params=params, data=data)

    def create_recipe_from_image(
        self,
        data: dict,
        translate_language: Any | None = None,
        accept_language: Any | None = None,
    ) -> Any:
        """Create Recipe From Image"""
        params: dict[str, Any] = {}
        if translate_language is not None:
            params["translateLanguage"] = translate_language
        return self.request(
            "POST", "/api/recipes/create/image", params=params, data=data
        )

    def get_recipes(
        self,
        categories: Any | None = None,
        tags: Any | None = None,
        tools: Any | None = None,
        foods: Any | None = None,
        households: Any | None = None,
        order_by: Any | None = None,
        order_by_null_position: Any | None = None,
        order_direction: Any | None = None,
        query_filter: Any | None = None,
        pagination_seed: Any | None = None,
        page: int | None = None,
        per_page: int | None = None,
        cookbook: Any | None = None,
        require_all_categories: bool | None = None,
        require_all_tags: bool | None = None,
        require_all_tools: bool | None = None,
        require_all_foods: bool | None = None,
        search: Any | None = None,
        accept_language: Any | None = None,
    ) -> Any:
        """Get All"""
        params: dict[str, Any] = {}
        if categories is not None:
            params["categories"] = categories
        if tags is not None:
            params["tags"] = tags
        if tools is not None:
            params["tools"] = tools
        if foods is not None:
            params["foods"] = foods
        if households is not None:
            params["households"] = households
        if order_by is not None:
            params["orderBy"] = order_by
        if order_by_null_position is not None:
            params["orderByNullPosition"] = order_by_null_position
        if order_direction is not None:
            params["orderDirection"] = order_direction
        if query_filter is not None:
            params["queryFilter"] = query_filter
        if pagination_seed is not None:
            params["paginationSeed"] = pagination_seed
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["perPage"] = per_page
        if cookbook is not None:
            params["cookbook"] = cookbook
        if require_all_categories is not None:
            params["requireAllCategories"] = require_all_categories
        if require_all_tags is not None:
            params["requireAllTags"] = require_all_tags
        if require_all_tools is not None:
            params["requireAllTools"] = require_all_tools
        if require_all_foods is not None:
            params["requireAllFoods"] = require_all_foods
        if search is not None:
            params["search"] = search
        return self.request("GET", "/api/recipes", params=params, data=None)

    def post_recipes(self, data: dict, accept_language: Any | None = None) -> Any:
        """Create One"""
        params = None
        return self.request("POST", "/api/recipes", params=params, data=data)

    def put_recipes(self, data: dict, accept_language: Any | None = None) -> Any:
        """Update Many"""
        params = None
        return self.request("PUT", "/api/recipes", params=params, data=data)

    def patch_many(self, data: dict, accept_language: Any | None = None) -> Any:
        """Patch Many"""
        params = None
        return self.request("PATCH", "/api/recipes", params=params, data=data)

    def get_recipes_suggestions(
        self,
        foods: Any | None = None,
        tools: Any | None = None,
        order_by: Any | None = None,
        order_by_null_position: Any | None = None,
        order_direction: Any | None = None,
        query_filter: Any | None = None,
        pagination_seed: Any | None = None,
        limit: int | None = None,
        max_missing_foods: int | None = None,
        max_missing_tools: int | None = None,
        include_foods_on_hand: bool | None = None,
        include_tools_on_hand: bool | None = None,
        accept_language: Any | None = None,
    ) -> Any:
        """Suggest Recipes"""
        params: dict[str, Any] = {}
        if foods is not None:
            params["foods"] = foods
        if tools is not None:
            params["tools"] = tools
        if order_by is not None:
            params["orderBy"] = order_by
        if order_by_null_position is not None:
            params["orderByNullPosition"] = order_by_null_position
        if order_direction is not None:
            params["orderDirection"] = order_direction
        if query_filter is not None:
            params["queryFilter"] = query_filter
        if pagination_seed is not None:
            params["paginationSeed"] = pagination_seed
        if limit is not None:
            params["limit"] = limit
        if max_missing_foods is not None:
            params["maxMissingFoods"] = max_missing_foods
        if max_missing_tools is not None:
            params["maxMissingTools"] = max_missing_tools
        if include_foods_on_hand is not None:
            params["includeFoodsOnHand"] = include_foods_on_hand
        if include_tools_on_hand is not None:
            params["includeToolsOnHand"] = include_tools_on_hand
        return self.request("GET", "/api/recipes/suggestions", params=params, data=None)

    def get_recipes_slug(self, slug: str, accept_language: Any | None = None) -> Any:
        """Get One"""
        params = None
        return self.request("GET", f"/api/recipes/{slug}", params=params, data=None)

    def put_recipes_slug(
        self, slug: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request("PUT", f"/api/recipes/{slug}", params=params, data=data)

    def patch_one(
        self, slug: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Patch One"""
        params = None
        return self.request("PATCH", f"/api/recipes/{slug}", params=params, data=data)

    def delete_recipes_slug(self, slug: str, accept_language: Any | None = None) -> Any:
        """Delete One"""
        params = None
        return self.request("DELETE", f"/api/recipes/{slug}", params=params, data=None)

    def duplicate_one(
        self, slug: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Duplicate One"""
        params = None
        return self.request(
            "POST", f"/api/recipes/{slug}/duplicate", params=params, data=data
        )

    def update_last_made(
        self, slug: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update Last Made"""
        params = None
        return self.request(
            "PATCH", f"/api/recipes/{slug}/last-made", params=params, data=data
        )

    def scrape_image_url(
        self, slug: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Scrape Image Url"""
        params = None
        return self.request(
            "POST", f"/api/recipes/{slug}/image", params=params, data=data
        )

    def update_recipe_image(
        self, slug: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update Recipe Image"""
        params = None
        return self.request(
            "PUT", f"/api/recipes/{slug}/image", params=params, data=data
        )

    def delete_recipe_image(self, slug: str, accept_language: Any | None = None) -> Any:
        """Delete Recipe Image"""
        params = None
        return self.request(
            "DELETE", f"/api/recipes/{slug}/image", params=params, data=None
        )

    def upload_recipe_asset(
        self, slug: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Upload Recipe Asset"""
        params = None
        return self.request(
            "POST", f"/api/recipes/{slug}/assets", params=params, data=data
        )

    def get_recipe_comments(self, slug: str, accept_language: Any | None = None) -> Any:
        """Get Recipe Comments"""
        params = None
        return self.request(
            "GET", f"/api/recipes/{slug}/comments", params=params, data=None
        )

    def bulk_tag_recipes(self, data: dict, accept_language: Any | None = None) -> Any:
        """Bulk Tag Recipes"""
        params = None
        return self.request(
            "POST", "/api/recipes/bulk-actions/tag", params=params, data=data
        )

    def bulk_settings_recipes(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Bulk Settings Recipes"""
        params = None
        return self.request(
            "POST", "/api/recipes/bulk-actions/settings", params=params, data=data
        )

    def bulk_categorize_recipes(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Bulk Categorize Recipes"""
        params = None
        return self.request(
            "POST", "/api/recipes/bulk-actions/categorize", params=params, data=data
        )

    def bulk_delete_recipes(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Bulk Delete Recipes"""
        params = None
        return self.request(
            "POST", "/api/recipes/bulk-actions/delete", params=params, data=data
        )

    def bulk_export_recipes(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Bulk Export Recipes"""
        params = None
        return self.request(
            "POST", "/api/recipes/bulk-actions/export", params=params, data=data
        )

    def get_exported_data(self, accept_language: Any | None = None) -> Any:
        """Get Exported Data"""
        params = None
        return self.request(
            "GET", "/api/recipes/bulk-actions/export", params=params, data=None
        )

    def get_exported_data_token(
        self, export_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get Exported Data Token"""
        params = None
        return self.request(
            "GET",
            f"/api/recipes/bulk-actions/export/{export_id}/download",
            params=params,
            data=None,
        )

    def purge_export_data(self, accept_language: Any | None = None) -> Any:
        """Purge Export Data"""
        params = None
        return self.request(
            "DELETE",
            "/api/recipes/bulk-actions/export/purge",
            params=params,
            data=None,
        )

    def get_shared_recipe(self, token_id: str) -> Any:
        """Get Shared Recipe"""
        params = None
        return self.request(
            "GET", f"/api/recipes/shared/{token_id}", params=params, data=None
        )

    def get_shared_recipe_as_zip(self, token_id: str) -> Any:
        """Get Shared Recipe As Zip"""
        params = None
        return self.request(
            "GET", f"/api/recipes/shared/{token_id}/zip", params=params, data=None
        )

    def get_recipes_timeline_events(
        self,
        order_by: Any | None = None,
        order_by_null_position: Any | None = None,
        order_direction: Any | None = None,
        query_filter: Any | None = None,
        pagination_seed: Any | None = None,
        page: int | None = None,
        per_page: int | None = None,
        accept_language: Any | None = None,
    ) -> Any:
        """Get All"""
        params: dict[str, Any] = {}
        if order_by is not None:
            params["orderBy"] = order_by
        if order_by_null_position is not None:
            params["orderByNullPosition"] = order_by_null_position
        if order_direction is not None:
            params["orderDirection"] = order_direction
        if query_filter is not None:
            params["queryFilter"] = query_filter
        if pagination_seed is not None:
            params["paginationSeed"] = pagination_seed
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["perPage"] = per_page
        return self.request(
            "GET", "/api/recipes/timeline/events", params=params, data=None
        )

    def post_recipes_timeline_events(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create One"""
        params = None
        return self.request(
            "POST", "/api/recipes/timeline/events", params=params, data=data
        )

    def get_recipes_timeline_events_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/recipes/timeline/events/{item_id}", params=params, data=None
        )

    def put_recipes_timeline_events_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request(
            "PUT", f"/api/recipes/timeline/events/{item_id}", params=params, data=data
        )

    def delete_recipes_timeline_events_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE",
            f"/api/recipes/timeline/events/{item_id}",
            params=params,
            data=None,
        )

    def update_event_image(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update Event Image"""
        params = None
        return self.request(
            "PUT",
            f"/api/recipes/timeline/events/{item_id}/image",
            params=params,
            data=data,
        )

    def get_comments(
        self,
        order_by: Any | None = None,
        order_by_null_position: Any | None = None,
        order_direction: Any | None = None,
        query_filter: Any | None = None,
        pagination_seed: Any | None = None,
        page: int | None = None,
        per_page: int | None = None,
        accept_language: Any | None = None,
    ) -> Any:
        """Get All"""
        params: dict[str, Any] = {}
        if order_by is not None:
            params["orderBy"] = order_by
        if order_by_null_position is not None:
            params["orderByNullPosition"] = order_by_null_position
        if order_direction is not None:
            params["orderDirection"] = order_direction
        if query_filter is not None:
            params["queryFilter"] = query_filter
        if pagination_seed is not None:
            params["paginationSeed"] = pagination_seed
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["perPage"] = per_page
        return self.request("GET", "/api/comments", params=params, data=None)

    def post_comments(self, data: dict, accept_language: Any | None = None) -> Any:
        """Create One"""
        params = None
        return self.request("POST", "/api/comments", params=params, data=data)

    def get_comments_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request("GET", f"/api/comments/{item_id}", params=params, data=None)

    def put_comments_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request("PUT", f"/api/comments/{item_id}", params=params, data=data)

    def post_parser_ingredient(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/comments/{item_id}", params=params, data=None
        )

    def parse_ingredient(self, data: dict, accept_language: Any | None = None) -> Any:
        """Parse Ingredient"""
        params = None
        return self.request("POST", "/api/parser/ingredient", params=params, data=data)

    def parse_ingredients(self, data: dict, accept_language: Any | None = None) -> Any:
        """Parse Ingredients"""
        params = None
        return self.request("POST", "/api/parser/ingredients", params=params, data=data)

    def get_foods(
        self,
        search: Any | None = None,
        order_by: Any | None = None,
        order_by_null_position: Any | None = None,
        order_direction: Any | None = None,
        query_filter: Any | None = None,
        pagination_seed: Any | None = None,
        page: int | None = None,
        per_page: int | None = None,
        accept_language: Any | None = None,
    ) -> Any:
        """Get All"""
        params: dict[str, Any] = {}
        if search is not None:
            params["search"] = search
        if order_by is not None:
            params["orderBy"] = order_by
        if order_by_null_position is not None:
            params["orderByNullPosition"] = order_by_null_position
        if order_direction is not None:
            params["orderDirection"] = order_direction
        if query_filter is not None:
            params["queryFilter"] = query_filter
        if pagination_seed is not None:
            params["paginationSeed"] = pagination_seed
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["perPage"] = per_page
        return self.request("GET", "/api/foods", params=params, data=None)

    def post_foods(self, data: dict, accept_language: Any | None = None) -> Any:
        """Create One"""
        params = None
        return self.request("POST", "/api/foods", params=params, data=data)

    def put_foods_merge(self, data: dict, accept_language: Any | None = None) -> Any:
        """Merge One"""
        params = None
        return self.request("PUT", "/api/foods/merge", params=params, data=data)

    def get_foods_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request("GET", f"/api/foods/{item_id}", params=params, data=None)

    def put_foods_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request("PUT", f"/api/foods/{item_id}", params=params, data=data)

    def delete_foods_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request("DELETE", f"/api/foods/{item_id}", params=params, data=None)

    def get_units(
        self,
        search: Any | None = None,
        order_by: Any | None = None,
        order_by_null_position: Any | None = None,
        order_direction: Any | None = None,
        query_filter: Any | None = None,
        pagination_seed: Any | None = None,
        page: int | None = None,
        per_page: int | None = None,
        accept_language: Any | None = None,
    ) -> Any:
        """Get All"""
        params: dict[str, Any] = {}
        if search is not None:
            params["search"] = search
        if order_by is not None:
            params["orderBy"] = order_by
        if order_by_null_position is not None:
            params["orderByNullPosition"] = order_by_null_position
        if order_direction is not None:
            params["orderDirection"] = order_direction
        if query_filter is not None:
            params["queryFilter"] = query_filter
        if pagination_seed is not None:
            params["paginationSeed"] = pagination_seed
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["perPage"] = per_page
        return self.request("GET", "/api/units", params=params, data=None)

    def post_units(self, data: dict, accept_language: Any | None = None) -> Any:
        """Create One"""
        params = None
        return self.request("POST", "/api/units", params=params, data=data)

    def put_units_merge(self, data: dict, accept_language: Any | None = None) -> Any:
        """Merge One"""
        params = None
        return self.request("PUT", "/api/units/merge", params=params, data=data)

    def get_units_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request("GET", f"/api/units/{item_id}", params=params, data=None)

    def put_units_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request("PUT", f"/api/units/{item_id}", params=params, data=data)

    def delete_units_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request("DELETE", f"/api/units/{item_id}", params=params, data=None)

    def get_recipe_img(self, recipe_id: str, file_name: Any) -> Any:
        """Get Recipe Img"""
        params = None
        return self.request(
            "GET",
            f"/api/media/recipes/{recipe_id}/images/{file_name}",
            params=params,
            data=None,
        )

    def get_recipe_timeline_event_img(
        self, recipe_id: str, timeline_event_id: str, file_name: Any
    ) -> Any:
        """Get Recipe Timeline Event Img"""
        params = None
        return self.request(
            "GET",
            f"/api/media/recipes/{recipe_id}/images/timeline/{timeline_event_id}/{file_name}",
            params=params,
            data=None,
        )

    def get_recipe_asset(self, recipe_id: str, file_name: str) -> Any:
        """Get Recipe Asset"""
        params = None
        return self.request(
            "GET",
            f"/api/media/recipes/{recipe_id}/assets/{file_name}",
            params=params,
            data=None,
        )

    def get_user_image(self, user_id: str, file_name: str) -> Any:
        """Get User Image"""
        params = None
        return self.request(
            "GET", f"/api/media/users/{user_id}/{file_name}", params=params, data=None
        )

    def get_validation_text(self) -> Any:
        """Get Validation Text"""
        params = None
        return self.request(
            "GET", "/api/media/docker/validate.txt", params=params, data=None
        )
