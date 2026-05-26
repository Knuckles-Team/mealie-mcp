#!/usr/bin/env python
from typing import Any

from mealie_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def get_all_households(
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
        """Get All Households"""
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
        return self.request("GET", "/api/groups/households", params=params, data=None)

    def get_one_household(
        self, household_slug: str, accept_language: Any | None = None
    ) -> Any:
        """Get One Household"""
        params = None
        return self.request(
            "GET", f"/api/groups/households/{household_slug}", params=params, data=None
        )

    def get_logged_in_user_group(self, accept_language: Any | None = None) -> Any:
        """Get Logged In User Group"""
        params = None
        return self.request("GET", "/api/groups/self", params=params, data=None)

    def get_group_members(
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
        """Get Group Members"""
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
        return self.request("GET", "/api/groups/members", params=params, data=None)

    def get_group_member(
        self, username_or_id: Any, accept_language: Any | None = None
    ) -> Any:
        """Get Group Member"""
        params = None
        return self.request(
            "GET", f"/api/groups/members/{username_or_id}", params=params, data=None
        )

    def get_group_preferences(self, accept_language: Any | None = None) -> Any:
        """Get Group Preferences"""
        params = None
        return self.request("GET", "/api/groups/preferences", params=params, data=None)

    def update_group_preferences(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update Group Preferences"""
        params = None
        return self.request("PUT", "/api/groups/preferences", params=params, data=data)

    def get_storage(self, accept_language: Any | None = None) -> Any:
        """Get Storage"""
        params = None
        return self.request("GET", "/api/groups/storage", params=params, data=None)

    def start_data_migration(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Start Data Migration"""
        params = None
        return self.request("POST", "/api/groups/migrations", params=params, data=data)

    def get_groups_reports(
        self, report_type: Any | None = None, accept_language: Any | None = None
    ) -> Any:
        """Get All"""
        params: dict[str, Any] = {}
        if report_type is not None:
            params["report_type"] = report_type
        return self.request("GET", "/api/groups/reports", params=params, data=None)

    def get_groups_reports_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/groups/reports/{item_id}", params=params, data=None
        )

    def delete_groups_reports_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/groups/reports/{item_id}", params=params, data=None
        )

    def get_groups_labels(
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
        return self.request("GET", "/api/groups/labels", params=params, data=None)

    def post_groups_labels(self, data: dict, accept_language: Any | None = None) -> Any:
        """Create One"""
        params = None
        return self.request("POST", "/api/groups/labels", params=params, data=data)

    def get_groups_labels_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/groups/labels/{item_id}", params=params, data=None
        )

    def put_groups_labels_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request(
            "PUT", f"/api/groups/labels/{item_id}", params=params, data=data
        )

    def delete_groups_labels_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/groups/labels/{item_id}", params=params, data=None
        )

    def seed_foods(self, data: dict, accept_language: Any | None = None) -> Any:
        """Seed Foods"""
        params = None
        return self.request(
            "POST", "/api/groups/seeders/foods", params=params, data=data
        )

    def seed_labels(self, data: dict, accept_language: Any | None = None) -> Any:
        """Seed Labels"""
        params = None
        return self.request(
            "POST", "/api/groups/seeders/labels", params=params, data=data
        )

    def seed_units(self, data: dict, accept_language: Any | None = None) -> Any:
        """Seed Units"""
        params = None
        return self.request(
            "POST", "/api/groups/seeders/units", params=params, data=data
        )
