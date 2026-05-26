#!/usr/bin/env python
from typing import Any

from mealie_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def get_shared_recipes(
        self, recipe_id: Any | None = None, accept_language: Any | None = None
    ) -> Any:
        """Get All"""
        params: dict[str, Any] = {}
        if recipe_id is not None:
            params["recipe_id"] = recipe_id
        return self.request("GET", "/api/shared/recipes", params=params, data=None)

    def post_shared_recipes(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create One"""
        params = None
        return self.request("POST", "/api/shared/recipes", params=params, data=data)

    def get_shared_recipes_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/shared/recipes/{item_id}", params=params, data=None
        )

    def delete_shared_recipes_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/shared/recipes/{item_id}", params=params, data=None
        )
