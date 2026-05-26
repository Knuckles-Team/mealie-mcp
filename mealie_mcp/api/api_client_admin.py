#!/usr/bin/env python
from typing import Any

from mealie_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def get_app_info(self, accept_language: Any | None = None) -> Any:
        """Get App Info"""
        params = None
        return self.request("GET", "/api/admin/about", params=params, data=None)

    def get_app_statistics(self, accept_language: Any | None = None) -> Any:
        """Get App Statistics"""
        params = None
        return self.request(
            "GET", "/api/admin/about/statistics", params=params, data=None
        )

    def check_app_config(self, accept_language: Any | None = None) -> Any:
        """Check App Config"""
        params = None
        return self.request("GET", "/api/admin/about/check", params=params, data=None)

    def get_admin_users(
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
        return self.request("GET", "/api/admin/users", params=params, data=None)

    def post_admin_users(self, data: dict, accept_language: Any | None = None) -> Any:
        """Create One"""
        params = None
        return self.request("POST", "/api/admin/users", params=params, data=data)

    def unlock_users(
        self, force: bool | None = None, accept_language: Any | None = None
    ) -> Any:
        """Unlock Users"""
        params: dict[str, Any] = {}
        if force is not None:
            params["force"] = force
        return self.request("POST", "/api/admin/users/unlock", params=params, data=None)

    def get_admin_users_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/admin/users/{item_id}", params=params, data=None
        )

    def put_admin_users_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request(
            "PUT", f"/api/admin/users/{item_id}", params=params, data=data
        )

    def generate_token(self, data: dict, accept_language: Any | None = None) -> Any:
        """Generate Token"""
        params = None
        return self.request(
            "POST", "/api/admin/users/password-reset-token", params=params, data=data
        )

    def delete_admin_users_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/admin/users/{item_id}", params=params, data=None
        )

    def get_admin_households(
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
        return self.request("GET", "/api/admin/households", params=params, data=None)

    def post_admin_households(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create One"""
        params = None
        return self.request("POST", "/api/admin/households", params=params, data=data)

    def get_admin_households_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/admin/households/{item_id}", params=params, data=None
        )

    def put_admin_households_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request(
            "PUT", f"/api/admin/households/{item_id}", params=params, data=data
        )

    def delete_admin_households_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/admin/households/{item_id}", params=params, data=None
        )

    def get_admin_groups(
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
        return self.request("GET", "/api/admin/groups", params=params, data=None)

    def post_admin_groups(self, data: dict, accept_language: Any | None = None) -> Any:
        """Create One"""
        params = None
        return self.request("POST", "/api/admin/groups", params=params, data=data)

    def get_admin_groups_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/admin/groups/{item_id}", params=params, data=None
        )

    def put_admin_groups_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request(
            "PUT", f"/api/admin/groups/{item_id}", params=params, data=data
        )

    def delete_admin_groups_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/admin/groups/{item_id}", params=params, data=None
        )

    def check_email_config(self, accept_language: Any | None = None) -> Any:
        """Check Email Config"""
        params = None
        return self.request("GET", "/api/admin/email", params=params, data=None)

    def send_test_email(self, data: dict, accept_language: Any | None = None) -> Any:
        """Send Test Email"""
        params = None
        return self.request("POST", "/api/admin/email", params=params, data=data)

    def get_admin_backups(self, accept_language: Any | None = None) -> Any:
        """Get All"""
        params = None
        return self.request("GET", "/api/admin/backups", params=params, data=None)

    def post_admin_backups(self, accept_language: Any | None = None) -> Any:
        """Create One"""
        params = None
        return self.request("POST", "/api/admin/backups", params=params, data=None)

    def get_admin_backups_file_name(
        self, file_name: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/admin/backups/{file_name}", params=params, data=None
        )

    def delete_admin_backups_file_name(
        self, file_name: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/admin/backups/{file_name}", params=params, data=None
        )

    def upload_one(self, data: dict, accept_language: Any | None = None) -> Any:
        """Upload One"""
        params = None
        return self.request(
            "POST", "/api/admin/backups/upload", params=params, data=data
        )

    def import_one(self, file_name: str, accept_language: Any | None = None) -> Any:
        """Import One"""
        params = None
        return self.request(
            "POST", f"/api/admin/backups/{file_name}/restore", params=params, data=None
        )

    def get_maintenance_summary(self, accept_language: Any | None = None) -> Any:
        """Get Maintenance Summary"""
        params = None
        return self.request("GET", "/api/admin/maintenance", params=params, data=None)

    def get_storage_details(self, accept_language: Any | None = None) -> Any:
        """Get Storage Details"""
        params = None
        return self.request(
            "GET", "/api/admin/maintenance/storage", params=params, data=None
        )

    def clean_images(self, accept_language: Any | None = None) -> Any:
        """Clean Images"""
        params = None
        return self.request(
            "POST", "/api/admin/maintenance/clean/images", params=params, data=None
        )

    def clean_temp(self, accept_language: Any | None = None) -> Any:
        """Clean Temp"""
        params = None
        return self.request(
            "POST", "/api/admin/maintenance/clean/temp", params=params, data=None
        )

    def clean_recipe_folders(self, accept_language: Any | None = None) -> Any:
        """Clean Recipe Folders"""
        params = None
        return self.request(
            "POST",
            "/api/admin/maintenance/clean/recipe-folders",
            params=params,
            data=None,
        )

    def debug_openai(
        self, accept_language: Any | None = None, data: dict | None = None
    ) -> Any:
        """Debug Openai"""
        params = None
        return self.request("POST", "/api/admin/debug/openai", params=params, data=data)
