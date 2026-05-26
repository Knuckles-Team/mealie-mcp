#!/usr/bin/env python
from typing import Any

from mealie_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def get_token(self, data: dict | None = None) -> Any:
        """Get Token"""
        params = None
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

    def logout(self, accept_language: Any | None = None) -> Any:
        """Logout"""
        params = None
        return self.request("POST", "/api/auth/logout", params=params, data=None)

    def register_new_user(self, data: dict, accept_language: Any | None = None) -> Any:
        """Register New User"""
        params = None
        return self.request("POST", "/api/users/register", params=params, data=data)

    def get_logged_in_user(self, accept_language: Any | None = None) -> Any:
        """Get Logged In User"""
        params = None
        return self.request("GET", "/api/users/self", params=params, data=None)

    def get_logged_in_user_ratings(self, accept_language: Any | None = None) -> Any:
        """Get Logged In User Ratings"""
        params = None
        return self.request("GET", "/api/users/self/ratings", params=params, data=None)

    def get_logged_in_user_rating_for_recipe(
        self, recipe_id: str, accept_language: Any | None = None
    ) -> Any:
        """Get Logged In User Rating For Recipe"""
        params = None
        return self.request(
            "GET", f"/api/users/self/ratings/{recipe_id}", params=params, data=None
        )

    def get_logged_in_user_favorites(self, accept_language: Any | None = None) -> Any:
        """Get Logged In User Favorites"""
        params = None
        return self.request(
            "GET", "/api/users/self/favorites", params=params, data=None
        )

    def update_password(self, data: dict, accept_language: Any | None = None) -> Any:
        """Update Password"""
        params = None
        return self.request("PUT", "/api/users/password", params=params, data=data)

    def update_user(
        self, item_id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update User"""
        params = None
        return self.request("PUT", f"/api/users/{item_id}", params=params, data=data)

    def forgot_password(self, data: dict, accept_language: Any | None = None) -> Any:
        """Forgot Password"""
        params = None
        return self.request(
            "POST", "/api/users/forgot-password", params=params, data=data
        )

    def reset_password(self, data: dict) -> Any:
        """Reset Password"""
        params = None
        return self.request(
            "POST", "/api/users/reset-password", params=params, data=data
        )

    def update_user_image(
        self, id: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Update User Image"""
        params = None
        return self.request("POST", f"/api/users/{id}/image", params=params, data=data)

    def create(self, data: dict, accept_language: Any | None = None) -> Any:
        """Create Api Token"""
        params = None
        return self.request("POST", "/api/users/api-tokens", params=params, data=data)

    def delete(self, token_id: int, accept_language: Any | None = None) -> Any:
        """Delete Api Token"""
        params = None
        return self.request(
            "DELETE", f"/api/users/api-tokens/{token_id}", params=params, data=None
        )

    def get_ratings(self, id: str, accept_language: Any | None = None) -> Any:
        """Get Ratings"""
        params = None
        return self.request("GET", f"/api/users/{id}/ratings", params=params, data=None)

    def get_favorites(self, id: str, accept_language: Any | None = None) -> Any:
        """Get Favorites"""
        params = None
        return self.request(
            "GET", f"/api/users/{id}/favorites", params=params, data=None
        )

    def set_rating(
        self, id: str, slug: str, data: dict, accept_language: Any | None = None
    ) -> Any:
        """Set Rating"""
        params = None
        return self.request(
            "POST", f"/api/users/{id}/ratings/{slug}", params=params, data=data
        )

    def add_favorite(
        self, id: str, slug: str, accept_language: Any | None = None
    ) -> Any:
        """Add Favorite"""
        params = None
        return self.request(
            "POST", f"/api/users/{id}/favorites/{slug}", params=params, data=None
        )

    def remove_favorite(
        self, id: str, slug: str, accept_language: Any | None = None
    ) -> Any:
        """Remove Favorite"""
        params = None
        return self.request(
            "DELETE", f"/api/users/{id}/favorites/{slug}", params=params, data=None
        )
