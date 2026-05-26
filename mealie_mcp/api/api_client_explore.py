#!/usr/bin/env python
from typing import Any

from mealie_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def get_explore_groups_group_slug_foods(
        self,
        group_slug: str,
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
            "GET", f"/api/explore/groups/{group_slug}/foods", params=params, data=None
        )

    def get_explore_groups_group_slug_foods_item_id(
        self, item_id: str, group_slug: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET",
            f"/api/explore/groups/{group_slug}/foods/{item_id}",
            params=params,
            data=None,
        )

    def get_explore_groups_group_slug_households(
        self,
        group_slug: str,
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
            "GET",
            f"/api/explore/groups/{group_slug}/households",
            params=params,
            data=None,
        )

    def get_household(
        self, household_slug: str, group_slug: str, accept_language: Any | None = None
    ) -> Any:
        """Get Household"""
        params = None
        return self.request(
            "GET",
            f"/api/explore/groups/{group_slug}/households/{household_slug}",
            params=params,
            data=None,
        )

    def get_explore_groups_group_slug_organizers_categories(
        self,
        group_slug: str,
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
            "GET",
            f"/api/explore/groups/{group_slug}/organizers/categories",
            params=params,
            data=None,
        )

    def get_explore_groups_group_slug_organizers_categories_item_id(
        self, item_id: str, group_slug: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET",
            f"/api/explore/groups/{group_slug}/organizers/categories/{item_id}",
            params=params,
            data=None,
        )

    def get_explore_groups_group_slug_organizers_tags(
        self,
        group_slug: str,
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
            "GET",
            f"/api/explore/groups/{group_slug}/organizers/tags",
            params=params,
            data=None,
        )

    def get_explore_groups_group_slug_organizers_tags_item_id(
        self, item_id: str, group_slug: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET",
            f"/api/explore/groups/{group_slug}/organizers/tags/{item_id}",
            params=params,
            data=None,
        )

    def get_explore_groups_group_slug_cookbooks(
        self,
        group_slug: str,
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
            "GET",
            f"/api/explore/groups/{group_slug}/cookbooks",
            params=params,
            data=None,
        )

    def get_explore_groups_group_slug_cookbooks_item_id(
        self, item_id: Any, group_slug: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET",
            f"/api/explore/groups/{group_slug}/cookbooks/{item_id}",
            params=params,
            data=None,
        )

    def get_explore_groups_group_slug_recipes(
        self,
        group_slug: str,
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
        return self.request(
            "GET", f"/api/explore/groups/{group_slug}/recipes", params=params, data=None
        )

    def get_explore_groups_group_slug_recipes_suggestions(
        self,
        group_slug: str,
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
        return self.request(
            "GET",
            f"/api/explore/groups/{group_slug}/recipes/suggestions",
            params=params,
            data=None,
        )

    def get_recipe(
        self, recipe_slug: str, group_slug: str, accept_language: Any | None = None
    ) -> Any:
        """Get Recipe"""
        params = None
        return self.request(
            "GET",
            f"/api/explore/groups/{group_slug}/recipes/{recipe_slug}",
            params=params,
            data=None,
        )

    def get_explore_groups_group_slug_organizers_tools(
        self,
        group_slug: str,
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
            "GET",
            f"/api/explore/groups/{group_slug}/organizers/tools",
            params=params,
            data=None,
        )

    def get_explore_groups_group_slug_organizers_tools_item_id(
        self, item_id: str, group_slug: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET",
            f"/api/explore/groups/{group_slug}/organizers/tools/{item_id}",
            params=params,
            data=None,
        )
