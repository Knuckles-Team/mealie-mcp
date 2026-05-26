#!/usr/bin/env python
from typing import Any

from mealie_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def get_households_cookbooks(
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
            "GET", "/api/households/cookbooks", params=params, data=None
        )

    def post_households_cookbooks(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create One"""
        params = None
        return self.request(
            "POST", "/api/households/cookbooks", params=params, data=data
        )

    def put_households_cookbooks(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update Many"""
        params = None
        return self.request(
            "PUT", "/api/households/cookbooks", params=params, data=data
        )

    def get_households_cookbooks_item_id(
        self, item_id: Any, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/households/cookbooks/{item_id}", params=params, data=None
        )

    def put_households_cookbooks_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request(
            "PUT", f"/api/households/cookbooks/{item_id}", params=params, data=data
        )

    def delete_households_cookbooks_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/households/cookbooks/{item_id}", params=params, data=None
        )

    def get_households_events_notifications(
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
            "GET", "/api/households/events/notifications", params=params, data=None
        )

    def post_households_events_notifications(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create One"""
        params = None
        return self.request(
            "POST", "/api/households/events/notifications", params=params, data=data
        )

    def get_households_events_notifications_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET",
            f"/api/households/events/notifications/{item_id}",
            params=params,
            data=None,
        )

    def put_households_events_notifications_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request(
            "PUT",
            f"/api/households/events/notifications/{item_id}",
            params=params,
            data=data,
        )

    def delete_households_events_notifications_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE",
            f"/api/households/events/notifications/{item_id}",
            params=params,
            data=None,
        )

    def test_notification(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Test Notification"""
        params = None
        return self.request(
            "POST",
            f"/api/households/events/notifications/{item_id}/test",
            params=params,
            data=None,
        )

    def get_households_recipe_actions(
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
            "GET", "/api/households/recipe-actions", params=params, data=None
        )

    def post_households_recipe_actions(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create One"""
        params = None
        return self.request(
            "POST", "/api/households/recipe-actions", params=params, data=data
        )

    def get_households_recipe_actions_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/households/recipe-actions/{item_id}", params=params, data=None
        )

    def put_households_recipe_actions_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request(
            "PUT", f"/api/households/recipe-actions/{item_id}", params=params, data=data
        )

    def delete_households_recipe_actions_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE",
            f"/api/households/recipe-actions/{item_id}",
            params=params,
            data=None,
        )

    def trigger_action(
        self,
        item_id: str,
        recipe_slug: str,
        accept_language: Any | None = None,
        data: dict | None = None,
    ) -> Any:
        """Trigger Action"""
        params = None
        return self.request(
            "POST",
            f"/api/households/recipe-actions/{item_id}/trigger/{recipe_slug}",
            params=params,
            data=data,
        )

    def get_logged_in_user_household(self, accept_language: Any | None = None) -> Any:
        """Get Logged In User Household"""
        params = None
        return self.request("GET", "/api/households/self", params=params, data=None)

    def get_household_recipe(
        self, recipe_slug: str, accept_language: Any | None = None
    ) -> Any:
        """Get Household Recipe"""
        params = None
        return self.request(
            "GET",
            f"/api/households/self/recipes/{recipe_slug}",
            params=params,
            data=None,
        )

    def get_household_members(
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
        """Get Household Members"""
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
        return self.request("GET", "/api/households/members", params=params, data=None)

    def get_household_preferences(self, accept_language: Any | None = None) -> Any:
        """Get Household Preferences"""
        params = None
        return self.request(
            "GET", "/api/households/preferences", params=params, data=None
        )

    def update_household_preferences(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update Household Preferences"""
        params = None
        return self.request(
            "PUT", "/api/households/preferences", params=params, data=data
        )

    def set_member_permissions(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Set Member Permissions"""
        params = None
        return self.request(
            "PUT", "/api/households/permissions", params=params, data=data
        )

    def get_statistics(self, accept_language: Any | None = None) -> Any:
        """Get Statistics"""
        params = None
        return self.request(
            "GET", "/api/households/statistics", params=params, data=None
        )

    def get_invite_tokens(self, accept_language: Any | None = None) -> Any:
        """Get Invite Tokens"""
        params = None
        return self.request(
            "GET", "/api/households/invitations", params=params, data=None
        )

    def create_invite_token(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create Invite Token"""
        params = None
        return self.request(
            "POST", "/api/households/invitations", params=params, data=data
        )

    def email_invitation(self, data: dict, accept_language: Any | None = None) -> Any:
        """Email Invitation"""
        params = None
        return self.request(
            "POST", "/api/households/invitations/email", params=params, data=data
        )

    def get_households_shopping_lists(
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
            "GET", "/api/households/shopping/lists", params=params, data=None
        )

    def post_households_shopping_lists(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create One"""
        params = None
        return self.request(
            "POST", "/api/households/shopping/lists", params=params, data=data
        )

    def get_households_shopping_lists_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/households/shopping/lists/{item_id}", params=params, data=None
        )

    def put_households_shopping_lists_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request(
            "PUT", f"/api/households/shopping/lists/{item_id}", params=params, data=data
        )

    def delete_households_shopping_lists_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE",
            f"/api/households/shopping/lists/{item_id}",
            params=params,
            data=None,
        )

    def update_label_settings(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update Label Settings"""
        params = None
        return self.request(
            "PUT",
            f"/api/households/shopping/lists/{item_id}/label-settings",
            params=params,
            data=data,
        )

    def add_recipe_ingredients_to_list(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Add Recipe Ingredients To List"""
        params = None
        return self.request(
            "POST",
            f"/api/households/shopping/lists/{item_id}/recipe",
            params=params,
            data=data,
        )

    def add_single_recipe_ingredients_to_list(
        self,
        item_id: str,
        recipe_id: str,
        accept_language: Any | None = None,
        data: dict | None = None,
    ) -> Any:
        """Add Single Recipe Ingredients To List"""
        params = None
        return self.request(
            "POST",
            f"/api/households/shopping/lists/{item_id}/recipe/{recipe_id}",
            params=params,
            data=data,
        )

    def remove_recipe_ingredients_from_list(
        self,
        item_id: str,
        recipe_id: str,
        accept_language: Any | None = None,
        data: dict | None = None,
    ) -> Any:
        """Remove Recipe Ingredients From List"""
        params = None
        return self.request(
            "POST",
            f"/api/households/shopping/lists/{item_id}/recipe/{recipe_id}/delete",
            params=params,
            data=data,
        )

    def get_households_shopping_items(
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
            "GET", "/api/households/shopping/items", params=params, data=None
        )

    def post_households_shopping_items(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create One"""
        params = None
        return self.request(
            "POST", "/api/households/shopping/items", params=params, data=data
        )

    def put_households_shopping_items(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update Many"""
        params = None
        return self.request(
            "PUT", "/api/households/shopping/items", params=params, data=data
        )

    def delete_households_shopping_items(
        self, ids: list | None = None, accept_language: Any | None = None
    ) -> Any:
        """Delete Many"""
        params: dict[str, Any] = {}
        if ids is not None:
            params["ids"] = ids
        return self.request(
            "DELETE", "/api/households/shopping/items", params=params, data=None
        )

    def post_households_shopping_items_create_bulk(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create Many"""
        params = None
        return self.request(
            "POST",
            "/api/households/shopping/items/create-bulk",
            params=params,
            data=data,
        )

    def get_households_shopping_items_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/households/shopping/items/{item_id}", params=params, data=None
        )

    def put_households_shopping_items_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request(
            "PUT", f"/api/households/shopping/items/{item_id}", params=params, data=data
        )

    def delete_households_shopping_items_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE",
            f"/api/households/shopping/items/{item_id}",
            params=params,
            data=None,
        )

    def get_households_webhooks(
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
        return self.request("GET", "/api/households/webhooks", params=params, data=None)

    def post_households_webhooks(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create One"""
        params = None
        return self.request(
            "POST", "/api/households/webhooks", params=params, data=data
        )

    def rerun_webhooks(self, accept_language: Any | None = None) -> Any:
        """Rerun Webhooks"""
        params = None
        return self.request(
            "POST", "/api/households/webhooks/rerun", params=params, data=None
        )

    def get_households_webhooks_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/households/webhooks/{item_id}", params=params, data=None
        )

    def put_households_webhooks_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request(
            "PUT", f"/api/households/webhooks/{item_id}", params=params, data=data
        )

    def delete_households_webhooks_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/households/webhooks/{item_id}", params=params, data=None
        )

    def test_one(self, item_id: str, accept_language: Any | None = None) -> Any:
        """Test One"""
        params = None
        return self.request(
            "POST", f"/api/households/webhooks/{item_id}/test", params=params, data=None
        )

    def get_households_mealplans_rules(
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
            "GET", "/api/households/mealplans/rules", params=params, data=None
        )

    def post_households_mealplans_rules(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create One"""
        params = None
        return self.request(
            "POST", "/api/households/mealplans/rules", params=params, data=data
        )

    def get_households_mealplans_rules_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET",
            f"/api/households/mealplans/rules/{item_id}",
            params=params,
            data=None,
        )

    def put_households_mealplans_rules_item_id(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request(
            "PUT",
            f"/api/households/mealplans/rules/{item_id}",
            params=params,
            data=data,
        )

    def delete_households_mealplans_rules_item_id(
        self, item_id: str, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE",
            f"/api/households/mealplans/rules/{item_id}",
            params=params,
            data=None,
        )

    def get_households_mealplans(
        self,
        start_date: Any | None = None,
        end_date: Any | None = None,
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
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
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
            "GET", "/api/households/mealplans", params=params, data=None
        )

    def post_households_mealplans(
        self, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Create One"""
        params = None
        return self.request(
            "POST", "/api/households/mealplans", params=params, data=data
        )

    def get_todays_meals(self, accept_language: Any | None = None) -> Any:
        """Get Todays Meals"""
        params = None
        return self.request(
            "GET", "/api/households/mealplans/today", params=params, data=None
        )

    def create_random_meal(self, data: dict, accept_language: Any | None = None) -> Any:
        """Create Random Meal"""
        params = None
        return self.request(
            "POST", "/api/households/mealplans/random", params=params, data=data
        )

    def get_households_mealplans_item_id(
        self, item_id: int, accept_language: Any | None = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/households/mealplans/{item_id}", params=params, data=None
        )

    def put_households_mealplans_item_id(
        self, item_id: int, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update One"""
        params = None
        return self.request(
            "PUT", f"/api/households/mealplans/{item_id}", params=params, data=data
        )

    def delete_households_mealplans_item_id(
        self, item_id: int, accept_language: Any | None = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/households/mealplans/{item_id}", params=params, data=None
        )
