#!/usr/bin/env python
# coding: utf-8

import requests
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
import urllib3


class Api:
    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        verify: bool = False,
    ):
        self.base_url = base_url
        self.token = token
        self._session = requests.Session()
        self._session.verify = verify

        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if token:
            self._session.headers.update({"Authorization": f"Bearer {token}"})

    def request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        data: Dict = None,
        files: Dict = None,
    ) -> Any:
        url = urljoin(self.base_url, endpoint)

        response = self._session.request(
            method=method, url=url, params=params, json=data, files=files
        )

        if response.status_code >= 400:
            raise Exception(f"API error: {response.status_code} - {response.text}")

        # Try to parse JSON, fallback to text/success
        if response.status_code == 204:
            return {"status": "success"}

        try:
            return response.json()
        except Exception:
            return {"status": "success", "text": response.text}

    def get_startup_info(self) -> Any:
        """Get Startup Info"""
        params = None
        return self.request(
            "GET", "/api/app/about/startup-info", params=params, data=None
        )

    def get_app_theme(self) -> Any:
        """Get App Theme"""
        params = None
        return self.request("GET", "/api/app/about/theme", params=params, data=None)

    def get_token(self, data: Dict = None) -> Any:
        """Get Token"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/auth/token", params=params, data=data)

    def oauth_login(self) -> Any:
        """Oauth Login"""
        params = None
        return self.request("GET", "/api/auth/oauth", params=params, data=None)

    def oauth_callback(self) -> Any:
        """Oauth Callback"""
        params = None
        return self.request("GET", "/api/auth/oauth/callback", params=params, data=None)

    def refresh_token(self) -> Any:
        """Refresh Token"""
        params = None
        return self.request("GET", "/api/auth/refresh", params=params, data=None)

    def logout(self, accept_language: Any = None) -> Any:
        """Logout"""
        params = None
        return self.request("POST", "/api/auth/logout", params=params, data=None)

    def register_new_user(self, data: Dict, accept_language: Any = None) -> Any:
        """Register New User"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/users/register", params=params, data=data)

    def get_logged_in_user(self, accept_language: Any = None) -> Any:
        """Get Logged In User"""
        params = None
        return self.request("GET", "/api/users/self", params=params, data=None)

    def get_logged_in_user_ratings(self, accept_language: Any = None) -> Any:
        """Get Logged In User Ratings"""
        params = None
        return self.request("GET", "/api/users/self/ratings", params=params, data=None)

    def get_logged_in_user_rating_for_recipe(
        self, recipe_id: str, accept_language: Any = None
    ) -> Any:
        """Get Logged In User Rating For Recipe"""
        params = None
        return self.request(
            "GET", f"/api/users/self/ratings/{recipe_id}", params=params, data=None
        )

    def get_logged_in_user_favorites(self, accept_language: Any = None) -> Any:
        """Get Logged In User Favorites"""
        params = None
        return self.request(
            "GET", "/api/users/self/favorites", params=params, data=None
        )

    def update_password(self, data: Dict, accept_language: Any = None) -> Any:
        """Update Password"""
        params = None
        # Body data is passed directly
        return self.request("PUT", "/api/users/password", params=params, data=data)

    def update_user(self, item_id: str, data: Dict, accept_language: Any = None) -> Any:
        """Update User"""
        params = None
        # Body data is passed directly
        return self.request("PUT", f"/api/users/{item_id}", params=params, data=data)

    def forgot_password(self, data: Dict, accept_language: Any = None) -> Any:
        """Forgot Password"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/users/forgot-password", params=params, data=data
        )

    def reset_password(self, data: Dict) -> Any:
        """Reset Password"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/users/reset-password", params=params, data=data
        )

    def update_user_image(
        self, id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update User Image"""
        params = None
        # Body data is passed directly
        return self.request("POST", f"/api/users/{id}/image", params=params, data=data)

    def create(self, data: Dict, accept_language: Any = None) -> Any:
        """Create Api Token"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/users/api-tokens", params=params, data=data)

    def delete(self, token_id: int, accept_language: Any = None) -> Any:
        """Delete Api Token"""
        params = None
        return self.request(
            "DELETE", f"/api/users/api-tokens/{token_id}", params=params, data=None
        )

    def get_ratings(self, id: str, accept_language: Any = None) -> Any:
        """Get Ratings"""
        params = None
        return self.request("GET", f"/api/users/{id}/ratings", params=params, data=None)

    def get_favorites(self, id: str, accept_language: Any = None) -> Any:
        """Get Favorites"""
        params = None
        return self.request(
            "GET", f"/api/users/{id}/favorites", params=params, data=None
        )

    def set_rating(
        self, id: str, slug: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Set Rating"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", f"/api/users/{id}/ratings/{slug}", params=params, data=data
        )

    def add_favorite(self, id: str, slug: str, accept_language: Any = None) -> Any:
        """Add Favorite"""
        params = None
        return self.request(
            "POST", f"/api/users/{id}/favorites/{slug}", params=params, data=None
        )

    def remove_favorite(self, id: str, slug: str, accept_language: Any = None) -> Any:
        """Remove Favorite"""
        params = None
        return self.request(
            "DELETE", f"/api/users/{id}/favorites/{slug}", params=params, data=None
        )

    def get_households_cookbooks(
        self,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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

    def post_households_cookbooks(self, data: Dict, accept_language: Any = None) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/households/cookbooks", params=params, data=data
        )

    def put_households_cookbooks(self, data: Dict, accept_language: Any = None) -> Any:
        """Update Many"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", "/api/households/cookbooks", params=params, data=data
        )

    def get_households_cookbooks_item_id(
        self, item_id: Any, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/households/cookbooks/{item_id}", params=params, data=None
        )

    def put_households_cookbooks_item_id(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", f"/api/households/cookbooks/{item_id}", params=params, data=data
        )

    def delete_households_cookbooks_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/households/cookbooks/{item_id}", params=params, data=None
        )

    def get_households_events_notifications(
        self,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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
        self, data: Dict, accept_language: Any = None
    ) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/households/events/notifications", params=params, data=data
        )

    def get_households_events_notifications_item_id(
        self, item_id: str, accept_language: Any = None
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
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT",
            f"/api/households/events/notifications/{item_id}",
            params=params,
            data=data,
        )

    def delete_households_events_notifications_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE",
            f"/api/households/events/notifications/{item_id}",
            params=params,
            data=None,
        )

    def test_notification(self, item_id: str, accept_language: Any = None) -> Any:
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
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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
        self, data: Dict, accept_language: Any = None
    ) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/households/recipe-actions", params=params, data=data
        )

    def get_households_recipe_actions_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/households/recipe-actions/{item_id}", params=params, data=None
        )

    def put_households_recipe_actions_item_id(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", f"/api/households/recipe-actions/{item_id}", params=params, data=data
        )

    def delete_households_recipe_actions_item_id(
        self, item_id: str, accept_language: Any = None
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
        accept_language: Any = None,
        data: Dict = None,
    ) -> Any:
        """Trigger Action"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST",
            f"/api/households/recipe-actions/{item_id}/trigger/{recipe_slug}",
            params=params,
            data=data,
        )

    def get_logged_in_user_household(self, accept_language: Any = None) -> Any:
        """Get Logged In User Household"""
        params = None
        return self.request("GET", "/api/households/self", params=params, data=None)

    def get_household_recipe(
        self, recipe_slug: str, accept_language: Any = None
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
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get Household Members"""
        params = {}
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

    def get_household_preferences(self, accept_language: Any = None) -> Any:
        """Get Household Preferences"""
        params = None
        return self.request(
            "GET", "/api/households/preferences", params=params, data=None
        )

    def update_household_preferences(
        self, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update Household Preferences"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", "/api/households/preferences", params=params, data=data
        )

    def set_member_permissions(self, data: Dict, accept_language: Any = None) -> Any:
        """Set Member Permissions"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", "/api/households/permissions", params=params, data=data
        )

    def get_statistics(self, accept_language: Any = None) -> Any:
        """Get Statistics"""
        params = None
        return self.request(
            "GET", "/api/households/statistics", params=params, data=None
        )

    def get_invite_tokens(self, accept_language: Any = None) -> Any:
        """Get Invite Tokens"""
        params = None
        return self.request(
            "GET", "/api/households/invitations", params=params, data=None
        )

    def create_invite_token(self, data: Dict, accept_language: Any = None) -> Any:
        """Create Invite Token"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/households/invitations", params=params, data=data
        )

    def email_invitation(self, data: Dict, accept_language: Any = None) -> Any:
        """Email Invitation"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/households/invitations/email", params=params, data=data
        )

    def get_households_shopping_lists(
        self,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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
        self, data: Dict, accept_language: Any = None
    ) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/households/shopping/lists", params=params, data=data
        )

    def get_households_shopping_lists_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/households/shopping/lists/{item_id}", params=params, data=None
        )

    def put_households_shopping_lists_item_id(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", f"/api/households/shopping/lists/{item_id}", params=params, data=data
        )

    def delete_households_shopping_lists_item_id(
        self, item_id: str, accept_language: Any = None
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
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update Label Settings"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT",
            f"/api/households/shopping/lists/{item_id}/label-settings",
            params=params,
            data=data,
        )

    def add_recipe_ingredients_to_list(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Add Recipe Ingredients To List"""
        params = None
        # Body data is passed directly
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
        accept_language: Any = None,
        data: Dict = None,
    ) -> Any:
        """Add Single Recipe Ingredients To List"""
        params = None
        # Body data is passed directly
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
        accept_language: Any = None,
        data: Dict = None,
    ) -> Any:
        """Remove Recipe Ingredients From List"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST",
            f"/api/households/shopping/lists/{item_id}/recipe/{recipe_id}/delete",
            params=params,
            data=data,
        )

    def get_households_shopping_items(
        self,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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
        self, data: Dict, accept_language: Any = None
    ) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/households/shopping/items", params=params, data=data
        )

    def put_households_shopping_items(
        self, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update Many"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", "/api/households/shopping/items", params=params, data=data
        )

    def delete_households_shopping_items(
        self, ids: List = None, accept_language: Any = None
    ) -> Any:
        """Delete Many"""
        params = {}
        if ids is not None:
            params["ids"] = ids
        return self.request(
            "DELETE", "/api/households/shopping/items", params=params, data=None
        )

    def post_households_shopping_items_create_bulk(
        self, data: Dict, accept_language: Any = None
    ) -> Any:
        """Create Many"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST",
            "/api/households/shopping/items/create-bulk",
            params=params,
            data=data,
        )

    def get_households_shopping_items_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/households/shopping/items/{item_id}", params=params, data=None
        )

    def put_households_shopping_items_item_id(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", f"/api/households/shopping/items/{item_id}", params=params, data=data
        )

    def delete_households_shopping_items_item_id(
        self, item_id: str, accept_language: Any = None
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
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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

    def post_households_webhooks(self, data: Dict, accept_language: Any = None) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/households/webhooks", params=params, data=data
        )

    def rerun_webhooks(self, accept_language: Any = None) -> Any:
        """Rerun Webhooks"""
        params = None
        return self.request(
            "POST", "/api/households/webhooks/rerun", params=params, data=None
        )

    def get_households_webhooks_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/households/webhooks/{item_id}", params=params, data=None
        )

    def put_households_webhooks_item_id(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", f"/api/households/webhooks/{item_id}", params=params, data=data
        )

    def delete_households_webhooks_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/households/webhooks/{item_id}", params=params, data=None
        )

    def test_one(self, item_id: str, accept_language: Any = None) -> Any:
        """Test One"""
        params = None
        return self.request(
            "POST", f"/api/households/webhooks/{item_id}/test", params=params, data=None
        )

    def get_households_mealplans_rules(
        self,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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
        self, data: Dict, accept_language: Any = None
    ) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/households/mealplans/rules", params=params, data=data
        )

    def get_households_mealplans_rules_item_id(
        self, item_id: str, accept_language: Any = None
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
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT",
            f"/api/households/mealplans/rules/{item_id}",
            params=params,
            data=data,
        )

    def delete_households_mealplans_rules_item_id(
        self, item_id: str, accept_language: Any = None
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
        start_date: Any = None,
        end_date: Any = None,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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

    def post_households_mealplans(self, data: Dict, accept_language: Any = None) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/households/mealplans", params=params, data=data
        )

    def get_todays_meals(self, accept_language: Any = None) -> Any:
        """Get Todays Meals"""
        params = None
        return self.request(
            "GET", "/api/households/mealplans/today", params=params, data=None
        )

    def create_random_meal(self, data: Dict, accept_language: Any = None) -> Any:
        """Create Random Meal"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/households/mealplans/random", params=params, data=data
        )

    def get_households_mealplans_item_id(
        self, item_id: int, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/households/mealplans/{item_id}", params=params, data=None
        )

    def put_households_mealplans_item_id(
        self, item_id: int, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", f"/api/households/mealplans/{item_id}", params=params, data=data
        )

    def delete_households_mealplans_item_id(
        self, item_id: int, accept_language: Any = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/households/mealplans/{item_id}", params=params, data=None
        )

    def get_all_households(
        self,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All Households"""
        params = {}
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
        self, household_slug: str, accept_language: Any = None
    ) -> Any:
        """Get One Household"""
        params = None
        return self.request(
            "GET", f"/api/groups/households/{household_slug}", params=params, data=None
        )

    def get_logged_in_user_group(self, accept_language: Any = None) -> Any:
        """Get Logged In User Group"""
        params = None
        return self.request("GET", "/api/groups/self", params=params, data=None)

    def get_group_members(
        self,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get Group Members"""
        params = {}
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

    def get_group_member(self, username_or_id: Any, accept_language: Any = None) -> Any:
        """Get Group Member"""
        params = None
        return self.request(
            "GET", f"/api/groups/members/{username_or_id}", params=params, data=None
        )

    def get_group_preferences(self, accept_language: Any = None) -> Any:
        """Get Group Preferences"""
        params = None
        return self.request("GET", "/api/groups/preferences", params=params, data=None)

    def update_group_preferences(self, data: Dict, accept_language: Any = None) -> Any:
        """Update Group Preferences"""
        params = None
        # Body data is passed directly
        return self.request("PUT", "/api/groups/preferences", params=params, data=data)

    def get_storage(self, accept_language: Any = None) -> Any:
        """Get Storage"""
        params = None
        return self.request("GET", "/api/groups/storage", params=params, data=None)

    def start_data_migration(self, data: Dict, accept_language: Any = None) -> Any:
        """Start Data Migration"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/groups/migrations", params=params, data=data)

    def get_groups_reports(
        self, report_type: Any = None, accept_language: Any = None
    ) -> Any:
        """Get All"""
        params = {}
        if report_type is not None:
            params["report_type"] = report_type
        return self.request("GET", "/api/groups/reports", params=params, data=None)

    def get_groups_reports_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/groups/reports/{item_id}", params=params, data=None
        )

    def delete_groups_reports_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/groups/reports/{item_id}", params=params, data=None
        )

    def get_groups_labels(
        self,
        search: Any = None,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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

    def post_groups_labels(self, data: Dict, accept_language: Any = None) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/groups/labels", params=params, data=data)

    def get_groups_labels_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/groups/labels/{item_id}", params=params, data=None
        )

    def put_groups_labels_item_id(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", f"/api/groups/labels/{item_id}", params=params, data=data
        )

    def delete_groups_labels_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/groups/labels/{item_id}", params=params, data=None
        )

    def seed_foods(self, data: Dict, accept_language: Any = None) -> Any:
        """Seed Foods"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/groups/seeders/foods", params=params, data=data
        )

    def seed_labels(self, data: Dict, accept_language: Any = None) -> Any:
        """Seed Labels"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/groups/seeders/labels", params=params, data=data
        )

    def seed_units(self, data: Dict, accept_language: Any = None) -> Any:
        """Seed Units"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/groups/seeders/units", params=params, data=data
        )

    def get_recipe_formats_and_templates(self, accept_language: Any = None) -> Any:
        """Get Recipe Formats And Templates"""
        params = None
        return self.request("GET", "/api/recipes/exports", params=params, data=None)

    def get_recipe_as_format(
        self, slug: str, template_name: str, accept_language: Any = None
    ) -> Any:
        """Get Recipe As Format"""
        params = {}
        if template_name is not None:
            params["template_name"] = template_name
        return self.request(
            "GET", f"/api/recipes/{slug}/exports", params=params, data=None
        )

    def test_parse_recipe_url(self, data: Dict, accept_language: Any = None) -> Any:
        """Test Parse Recipe Url"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/recipes/test-scrape-url", params=params, data=data
        )

    def create_recipe_from_html_or_json(
        self, data: Dict, accept_language: Any = None
    ) -> Any:
        """Create Recipe From Html Or Json"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/recipes/create/html-or-json", params=params, data=data
        )

    def parse_recipe_url(self, data: Dict, accept_language: Any = None) -> Any:
        """Parse Recipe Url"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/recipes/create/url", params=params, data=data)

    def parse_recipe_url_bulk(self, data: Dict, accept_language: Any = None) -> Any:
        """Parse Recipe Url Bulk"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/recipes/create/url/bulk", params=params, data=data
        )

    def create_recipe_from_zip(self, data: Dict, accept_language: Any = None) -> Any:
        """Create Recipe From Zip"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/recipes/create/zip", params=params, data=data)

    def create_recipe_from_image(
        self, data: Dict, translate_language: Any = None, accept_language: Any = None
    ) -> Any:
        """Create Recipe From Image"""
        params = {}
        if translate_language is not None:
            params["translateLanguage"] = translate_language
        # Body data is passed directly
        return self.request(
            "POST", "/api/recipes/create/image", params=params, data=data
        )

    def get_recipes(
        self,
        categories: Any = None,
        tags: Any = None,
        tools: Any = None,
        foods: Any = None,
        households: Any = None,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        cookbook: Any = None,
        require_all_categories: bool = None,
        require_all_tags: bool = None,
        require_all_tools: bool = None,
        require_all_foods: bool = None,
        search: Any = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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

    def post_recipes(self, data: Dict, accept_language: Any = None) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/recipes", params=params, data=data)

    def put_recipes(self, data: Dict, accept_language: Any = None) -> Any:
        """Update Many"""
        params = None
        # Body data is passed directly
        return self.request("PUT", "/api/recipes", params=params, data=data)

    def patch_many(self, data: Dict, accept_language: Any = None) -> Any:
        """Patch Many"""
        params = None
        # Body data is passed directly
        return self.request("PATCH", "/api/recipes", params=params, data=data)

    def get_recipes_suggestions(
        self,
        foods: Any = None,
        tools: Any = None,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        limit: int = None,
        max_missing_foods: int = None,
        max_missing_tools: int = None,
        include_foods_on_hand: bool = None,
        include_tools_on_hand: bool = None,
        accept_language: Any = None,
    ) -> Any:
        """Suggest Recipes"""
        params = {}
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

    def get_recipes_slug(self, slug: str, accept_language: Any = None) -> Any:
        """Get One"""
        params = None
        return self.request("GET", f"/api/recipes/{slug}", params=params, data=None)

    def put_recipes_slug(
        self, slug: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request("PUT", f"/api/recipes/{slug}", params=params, data=data)

    def patch_one(self, slug: str, data: Dict, accept_language: Any = None) -> Any:
        """Patch One"""
        params = None
        # Body data is passed directly
        return self.request("PATCH", f"/api/recipes/{slug}", params=params, data=data)

    def delete_recipes_slug(self, slug: str, accept_language: Any = None) -> Any:
        """Delete One"""
        params = None
        return self.request("DELETE", f"/api/recipes/{slug}", params=params, data=None)

    def duplicate_one(self, slug: str, data: Dict, accept_language: Any = None) -> Any:
        """Duplicate One"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", f"/api/recipes/{slug}/duplicate", params=params, data=data
        )

    def update_last_made(
        self, slug: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update Last Made"""
        params = None
        # Body data is passed directly
        return self.request(
            "PATCH", f"/api/recipes/{slug}/last-made", params=params, data=data
        )

    def scrape_image_url(
        self, slug: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Scrape Image Url"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", f"/api/recipes/{slug}/image", params=params, data=data
        )

    def update_recipe_image(
        self, slug: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update Recipe Image"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", f"/api/recipes/{slug}/image", params=params, data=data
        )

    def delete_recipe_image(self, slug: str, accept_language: Any = None) -> Any:
        """Delete Recipe Image"""
        params = None
        return self.request(
            "DELETE", f"/api/recipes/{slug}/image", params=params, data=None
        )

    def upload_recipe_asset(
        self, slug: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Upload Recipe Asset"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", f"/api/recipes/{slug}/assets", params=params, data=data
        )

    def get_recipe_comments(self, slug: str, accept_language: Any = None) -> Any:
        """Get Recipe Comments"""
        params = None
        return self.request(
            "GET", f"/api/recipes/{slug}/comments", params=params, data=None
        )

    def bulk_tag_recipes(self, data: Dict, accept_language: Any = None) -> Any:
        """Bulk Tag Recipes"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/recipes/bulk-actions/tag", params=params, data=data
        )

    def bulk_settings_recipes(self, data: Dict, accept_language: Any = None) -> Any:
        """Bulk Settings Recipes"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/recipes/bulk-actions/settings", params=params, data=data
        )

    def bulk_categorize_recipes(self, data: Dict, accept_language: Any = None) -> Any:
        """Bulk Categorize Recipes"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/recipes/bulk-actions/categorize", params=params, data=data
        )

    def bulk_delete_recipes(self, data: Dict, accept_language: Any = None) -> Any:
        """Bulk Delete Recipes"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/recipes/bulk-actions/delete", params=params, data=data
        )

    def bulk_export_recipes(self, data: Dict, accept_language: Any = None) -> Any:
        """Bulk Export Recipes"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/recipes/bulk-actions/export", params=params, data=data
        )

    def get_exported_data(self, accept_language: Any = None) -> Any:
        """Get Exported Data"""
        params = None
        return self.request(
            "GET", "/api/recipes/bulk-actions/export", params=params, data=None
        )

    def get_exported_data_token(
        self, export_id: str, accept_language: Any = None
    ) -> Any:
        """Get Exported Data Token"""
        params = None
        return self.request(
            "GET",
            f"/api/recipes/bulk-actions/export/{export_id}/download",
            params=params,
            data=None,
        )

    def purge_export_data(self, accept_language: Any = None) -> Any:
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
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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
        self, data: Dict, accept_language: Any = None
    ) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/recipes/timeline/events", params=params, data=data
        )

    def get_recipes_timeline_events_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/recipes/timeline/events/{item_id}", params=params, data=None
        )

    def put_recipes_timeline_events_item_id(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", f"/api/recipes/timeline/events/{item_id}", params=params, data=data
        )

    def delete_recipes_timeline_events_item_id(
        self, item_id: str, accept_language: Any = None
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
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update Event Image"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT",
            f"/api/recipes/timeline/events/{item_id}/image",
            params=params,
            data=data,
        )

    def get_organizers_categories(
        self,
        search: Any = None,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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
        self, data: Dict, accept_language: Any = None
    ) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/organizers/categories", params=params, data=data
        )

    def get_all_empty(self, accept_language: Any = None) -> Any:
        """Get All Empty"""
        params = None
        return self.request(
            "GET", "/api/organizers/categories/empty", params=params, data=None
        )

    def get_organizers_categories_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/organizers/categories/{item_id}", params=params, data=None
        )

    def put_organizers_categories_item_id(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", f"/api/organizers/categories/{item_id}", params=params, data=data
        )

    def delete_organizers_categories_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/organizers/categories/{item_id}", params=params, data=None
        )

    def get_organizers_categories_slug_category_slug(
        self, category_slug: str, accept_language: Any = None
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
        search: Any = None,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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

    def post_organizers_tags(self, data: Dict, accept_language: Any = None) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/organizers/tags", params=params, data=data)

    def get_empty_tags(self, accept_language: Any = None) -> Any:
        """Get Empty Tags"""
        params = None
        return self.request(
            "GET", "/api/organizers/tags/empty", params=params, data=None
        )

    def get_organizers_tags_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/organizers/tags/{item_id}", params=params, data=None
        )

    def put_organizers_tags_item_id(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", f"/api/organizers/tags/{item_id}", params=params, data=data
        )

    def delete_recipe_tag(self, item_id: str, accept_language: Any = None) -> Any:
        """Delete Recipe Tag"""
        params = None
        return self.request(
            "DELETE", f"/api/organizers/tags/{item_id}", params=params, data=None
        )

    def get_organizers_tags_slug_tag_slug(
        self, tag_slug: str, accept_language: Any = None
    ) -> Any:
        """Get One By Slug"""
        params = None
        return self.request(
            "GET", f"/api/organizers/tags/slug/{tag_slug}", params=params, data=None
        )

    def get_organizers_tools(
        self,
        search: Any = None,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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

    def post_organizers_tools(self, data: Dict, accept_language: Any = None) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/organizers/tools", params=params, data=data)

    def get_organizers_tools_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/organizers/tools/{item_id}", params=params, data=None
        )

    def put_organizers_tools_item_id(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", f"/api/organizers/tools/{item_id}", params=params, data=data
        )

    def delete_organizers_tools_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/organizers/tools/{item_id}", params=params, data=None
        )

    def get_organizers_tools_slug_tool_slug(
        self, tool_slug: str, accept_language: Any = None
    ) -> Any:
        """Get One By Slug"""
        params = None
        return self.request(
            "GET", f"/api/organizers/tools/slug/{tool_slug}", params=params, data=None
        )

    def get_shared_recipes(
        self, recipe_id: Any = None, accept_language: Any = None
    ) -> Any:
        """Get All"""
        params = {}
        if recipe_id is not None:
            params["recipe_id"] = recipe_id
        return self.request("GET", "/api/shared/recipes", params=params, data=None)

    def post_shared_recipes(self, data: Dict, accept_language: Any = None) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/shared/recipes", params=params, data=data)

    def get_shared_recipes_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/shared/recipes/{item_id}", params=params, data=None
        )

    def delete_shared_recipes_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/shared/recipes/{item_id}", params=params, data=None
        )

    def get_comments(
        self,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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

    def post_comments(self, data: Dict, accept_language: Any = None) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/comments", params=params, data=data)

    def get_comments_item_id(self, item_id: str, accept_language: Any = None) -> Any:
        """Get One"""
        params = None
        return self.request("GET", f"/api/comments/{item_id}", params=params, data=None)

    def put_comments_item_id(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request("PUT", f"/api/comments/{item_id}", params=params, data=data)

    def post_parser_ingredient(self, item_id: str, accept_language: Any = None) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/comments/{item_id}", params=params, data=None
        )

    def parse_ingredient(self, data: Dict, accept_language: Any = None) -> Any:
        """Parse Ingredient"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/parser/ingredient", params=params, data=data)

    def parse_ingredients(self, data: Dict, accept_language: Any = None) -> Any:
        """Parse Ingredients"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/parser/ingredients", params=params, data=data)

    def get_foods(
        self,
        search: Any = None,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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

    def post_foods(self, data: Dict, accept_language: Any = None) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/foods", params=params, data=data)

    def put_foods_merge(self, data: Dict, accept_language: Any = None) -> Any:
        """Merge One"""
        params = None
        # Body data is passed directly
        return self.request("PUT", "/api/foods/merge", params=params, data=data)

    def get_foods_item_id(self, item_id: str, accept_language: Any = None) -> Any:
        """Get One"""
        params = None
        return self.request("GET", f"/api/foods/{item_id}", params=params, data=None)

    def put_foods_item_id(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request("PUT", f"/api/foods/{item_id}", params=params, data=data)

    def delete_foods_item_id(self, item_id: str, accept_language: Any = None) -> Any:
        """Delete One"""
        params = None
        return self.request("DELETE", f"/api/foods/{item_id}", params=params, data=None)

    def get_units(
        self,
        search: Any = None,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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

    def post_units(self, data: Dict, accept_language: Any = None) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/units", params=params, data=data)

    def put_units_merge(self, data: Dict, accept_language: Any = None) -> Any:
        """Merge One"""
        params = None
        # Body data is passed directly
        return self.request("PUT", "/api/units/merge", params=params, data=data)

    def get_units_item_id(self, item_id: str, accept_language: Any = None) -> Any:
        """Get One"""
        params = None
        return self.request("GET", f"/api/units/{item_id}", params=params, data=None)

    def put_units_item_id(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request("PUT", f"/api/units/{item_id}", params=params, data=data)

    def delete_units_item_id(self, item_id: str, accept_language: Any = None) -> Any:
        """Delete One"""
        params = None
        return self.request("DELETE", f"/api/units/{item_id}", params=params, data=None)

    def get_app_info(self, accept_language: Any = None) -> Any:
        """Get App Info"""
        params = None
        return self.request("GET", "/api/admin/about", params=params, data=None)

    def get_app_statistics(self, accept_language: Any = None) -> Any:
        """Get App Statistics"""
        params = None
        return self.request(
            "GET", "/api/admin/about/statistics", params=params, data=None
        )

    def check_app_config(self, accept_language: Any = None) -> Any:
        """Check App Config"""
        params = None
        return self.request("GET", "/api/admin/about/check", params=params, data=None)

    def get_admin_users(
        self,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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

    def post_admin_users(self, data: Dict, accept_language: Any = None) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/admin/users", params=params, data=data)

    def unlock_users(self, force: bool = None, accept_language: Any = None) -> Any:
        """Unlock Users"""
        params = {}
        if force is not None:
            params["force"] = force
        return self.request("POST", "/api/admin/users/unlock", params=params, data=None)

    def get_admin_users_item_id(self, item_id: str, accept_language: Any = None) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/admin/users/{item_id}", params=params, data=None
        )

    def put_admin_users_item_id(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", f"/api/admin/users/{item_id}", params=params, data=data
        )

    def generate_token(self, data: Dict, accept_language: Any = None) -> Any:
        """Generate Token"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/admin/users/password-reset-token", params=params, data=data
        )

    def delete_admin_users_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/admin/users/{item_id}", params=params, data=None
        )

    def get_admin_households(
        self,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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

    def post_admin_households(self, data: Dict, accept_language: Any = None) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/admin/households", params=params, data=data)

    def get_admin_households_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/admin/households/{item_id}", params=params, data=None
        )

    def put_admin_households_item_id(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", f"/api/admin/households/{item_id}", params=params, data=data
        )

    def delete_admin_households_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/admin/households/{item_id}", params=params, data=None
        )

    def get_admin_groups(
        self,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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

    def post_admin_groups(self, data: Dict, accept_language: Any = None) -> Any:
        """Create One"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/admin/groups", params=params, data=data)

    def get_admin_groups_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/admin/groups/{item_id}", params=params, data=None
        )

    def put_admin_groups_item_id(
        self, item_id: str, data: Dict, accept_language: Any = None
    ) -> Any:
        """Update One"""
        params = None
        # Body data is passed directly
        return self.request(
            "PUT", f"/api/admin/groups/{item_id}", params=params, data=data
        )

    def delete_admin_groups_item_id(
        self, item_id: str, accept_language: Any = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/admin/groups/{item_id}", params=params, data=None
        )

    def check_email_config(self, accept_language: Any = None) -> Any:
        """Check Email Config"""
        params = None
        return self.request("GET", "/api/admin/email", params=params, data=None)

    def send_test_email(self, data: Dict, accept_language: Any = None) -> Any:
        """Send Test Email"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/admin/email", params=params, data=data)

    def get_admin_backups(self, accept_language: Any = None) -> Any:
        """Get All"""
        params = None
        return self.request("GET", "/api/admin/backups", params=params, data=None)

    def post_admin_backups(self, accept_language: Any = None) -> Any:
        """Create One"""
        params = None
        return self.request("POST", "/api/admin/backups", params=params, data=None)

    def get_admin_backups_file_name(
        self, file_name: str, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET", f"/api/admin/backups/{file_name}", params=params, data=None
        )

    def delete_admin_backups_file_name(
        self, file_name: str, accept_language: Any = None
    ) -> Any:
        """Delete One"""
        params = None
        return self.request(
            "DELETE", f"/api/admin/backups/{file_name}", params=params, data=None
        )

    def upload_one(self, data: Dict, accept_language: Any = None) -> Any:
        """Upload One"""
        params = None
        # Body data is passed directly
        return self.request(
            "POST", "/api/admin/backups/upload", params=params, data=data
        )

    def import_one(self, file_name: str, accept_language: Any = None) -> Any:
        """Import One"""
        params = None
        return self.request(
            "POST", f"/api/admin/backups/{file_name}/restore", params=params, data=None
        )

    def get_maintenance_summary(self, accept_language: Any = None) -> Any:
        """Get Maintenance Summary"""
        params = None
        return self.request("GET", "/api/admin/maintenance", params=params, data=None)

    def get_storage_details(self, accept_language: Any = None) -> Any:
        """Get Storage Details"""
        params = None
        return self.request(
            "GET", "/api/admin/maintenance/storage", params=params, data=None
        )

    def clean_images(self, accept_language: Any = None) -> Any:
        """Clean Images"""
        params = None
        return self.request(
            "POST", "/api/admin/maintenance/clean/images", params=params, data=None
        )

    def clean_temp(self, accept_language: Any = None) -> Any:
        """Clean Temp"""
        params = None
        return self.request(
            "POST", "/api/admin/maintenance/clean/temp", params=params, data=None
        )

    def clean_recipe_folders(self, accept_language: Any = None) -> Any:
        """Clean Recipe Folders"""
        params = None
        return self.request(
            "POST",
            "/api/admin/maintenance/clean/recipe-folders",
            params=params,
            data=None,
        )

    def debug_openai(self, accept_language: Any = None, data: Dict = None) -> Any:
        """Debug Openai"""
        params = None
        # Body data is passed directly
        return self.request("POST", "/api/admin/debug/openai", params=params, data=data)

    def get_explore_groups_group_slug_foods(
        self,
        group_slug: str,
        search: Any = None,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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
        self, item_id: str, group_slug: str, accept_language: Any = None
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
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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
        self, household_slug: str, group_slug: str, accept_language: Any = None
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
        search: Any = None,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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
        self, item_id: str, group_slug: str, accept_language: Any = None
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
        search: Any = None,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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
        self, item_id: str, group_slug: str, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET",
            f"/api/explore/groups/{group_slug}/organizers/tags/{item_id}",
            params=params,
            data=None,
        )

    def get_explore_groups_group_slug_organizers_tools(
        self,
        group_slug: str,
        search: Any = None,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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
        self, item_id: str, group_slug: str, accept_language: Any = None
    ) -> Any:
        """Get One"""
        params = None
        return self.request(
            "GET",
            f"/api/explore/groups/{group_slug}/organizers/tools/{item_id}",
            params=params,
            data=None,
        )

    def get_explore_groups_group_slug_cookbooks(
        self,
        group_slug: str,
        search: Any = None,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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
        self, item_id: Any, group_slug: str, accept_language: Any = None
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
        categories: Any = None,
        tags: Any = None,
        tools: Any = None,
        foods: Any = None,
        households: Any = None,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        page: int = None,
        per_page: int = None,
        cookbook: Any = None,
        require_all_categories: bool = None,
        require_all_tags: bool = None,
        require_all_tools: bool = None,
        require_all_foods: bool = None,
        search: Any = None,
        accept_language: Any = None,
    ) -> Any:
        """Get All"""
        params = {}
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
        foods: Any = None,
        tools: Any = None,
        order_by: Any = None,
        order_by_null_position: Any = None,
        order_direction: Any = None,
        query_filter: Any = None,
        pagination_seed: Any = None,
        limit: int = None,
        max_missing_foods: int = None,
        max_missing_tools: int = None,
        include_foods_on_hand: bool = None,
        include_tools_on_hand: bool = None,
        accept_language: Any = None,
    ) -> Any:
        """Suggest Recipes"""
        params = {}
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
        self, recipe_slug: str, group_slug: str, accept_language: Any = None
    ) -> Any:
        """Get Recipe"""
        params = None
        return self.request(
            "GET",
            f"/api/explore/groups/{group_slug}/recipes/{recipe_slug}",
            params=params,
            data=None,
        )

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

    def download_file(self, token: Any = None) -> Any:
        """Download File"""
        params = {}
        if token is not None:
            params["token"] = token
        return self.request("GET", "/api/utils/download", params=params, data=None)
