#!/usr/bin/env python
from typing import Any

from mealie_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def get_organizers_categories(
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
        return self.request(
            "GET", "/api/organizers/categories", params=params, data=None
        )

    def post_organizers_categories(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create One"""
        params = None
        return self.request(
            "POST", "/api/organizers/categories", params=params, data=data
        )

    def get_all_empty(self, accept_language: Any | None = None) -> Any:
        """Get All Empty"""
        params = None
        return self.request(
            "GET", "/api/organizers/categories/empty", params=params, data=None
        )

    def get_organizers_categories_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/organizers/categories/{item_id}", params=params, data=None
        )

    def put_organizers_categories_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request(
            "PUT", f"/api/organizers/categories/{item_id}", params=params, data=data
        )

    def delete_organizers_categories_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/organizers/categories/{item_id}", params=params, data=None
        )

    def get_organizers_categories_slug_category_slug(
        self, category_slug: str, accept_language: Any | None = None
    ) -> Any:
        """Get One By Slug"""
        params = None
        return self.request(
            "GET",
            f"/api/organizers/categories/slug/{category_slug}",
            params=params,
            data=None,
        )

    def get_organizers_tags(
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
        return self.request("GET", "/api/organizers/tags", params=params, data=None)

    def post_organizers_tags(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create One"""
        params = None
        return self.request("POST", "/api/organizers/tags", params=params, data=data)

    def get_empty_tags(self, accept_language: Any | None = None) -> Any:
        """Get Empty Tags"""
        params = None
        return self.request(
            "GET", "/api/organizers/tags/empty", params=params, data=None
        )

    def get_organizers_tags_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/organizers/tags/{item_id}", params=params, data=None
        )

    def put_organizers_tags_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request(
            "PUT", f"/api/organizers/tags/{item_id}", params=params, data=data
        )

    def delete_recipe_tag(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete Recipe Tag"""
        params = None
        return self.request(
            "DELETE", f"/api/organizers/tags/{item_id}", params=params, data=None
        )

    def get_organizers_tags_slug_tag_slug(
        self, tag_slug: str, accept_language: Any | None = None
    ) -> Any:
        """Get One By Slug"""
        params = None
        return self.request(
            "GET", f"/api/organizers/tags/slug/{tag_slug}", params=params, data=None
        )

    def get_organizers_tools(
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
        return self.request("GET", "/api/organizers/tools", params=params, data=None)

    def post_organizers_tools(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create One"""
        params = None
        return self.request("POST", "/api/organizers/tools", params=params, data=data)

    def get_organizers_tools_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/organizers/tools/{item_id}", params=params, data=None
        )

    def put_organizers_tools_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request(
            "PUT", f"/api/organizers/tools/{item_id}", params=params, data=data
        )

    def delete_organizers_tools_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/organizers/tools/{item_id}", params=params, data=None
        )

    def get_organizers_tools_slug_tool_slug(
        self, tool_slug: str, accept_language: Any | None = None
    ) -> Any:
        """Get One By Slug"""
        params = None
        return self.request(
            "GET", f"/api/organizers/tools/slug/{tool_slug}", params=params, data=None
        )
