#!/usr/bin/python
# coding: utf-8

import os
import argparse
import sys
import logging
from typing import Optional, List, Dict, Union, Any

import requests
from pydantic import Field
from eunomia_mcp.middleware import EunomiaMcpMiddleware
from fastmcp import FastMCP, Context
from fastmcp.server.auth.oidc_proxy import OIDCProxy
from fastmcp.server.auth import OAuthProxy, RemoteAuthProvider
from fastmcp.server.auth.providers.jwt import JWTVerifier, StaticTokenVerifier
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.timing import TimingMiddleware
from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.utilities.logging import get_logger
from mealie_mcp.middlewares import (
    UserTokenMiddleware,
    JWTClaimsLoggingMiddleware,
)
from mealie_mcp.mealie_api import Api
from mealie_mcp.utils import to_boolean, to_integer

__version__ = "0.2.12"
print(f"Mealie MCP v{__version__}")

logger = get_logger(name="TokenMiddleware")
logger.setLevel(logging.DEBUG)

config = {
    "enable_delegation": to_boolean(os.environ.get("ENABLE_DELEGATION", "False")),
    "audience": os.environ.get("AUDIENCE", None),
    "delegated_scopes": os.environ.get("DELEGATED_SCOPES", "api"),
    "token_endpoint": None,
    "oidc_client_id": os.environ.get("OIDC_CLIENT_ID", None),
    "oidc_client_secret": os.environ.get("OIDC_CLIENT_SECRET", None),
    "oidc_config_url": os.environ.get("OIDC_CONFIG_URL", None),
    "jwt_jwks_uri": os.getenv("FASTMCP_SERVER_AUTH_JWT_JWKS_URI", None),
    "jwt_issuer": os.getenv("FASTMCP_SERVER_AUTH_JWT_ISSUER", None),
    "jwt_audience": os.getenv("FASTMCP_SERVER_AUTH_JWT_AUDIENCE", None),
    "jwt_algorithm": os.getenv("FASTMCP_SERVER_AUTH_JWT_ALGORITHM", None),
    "jwt_secret": os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY", None),
    "jwt_required_scopes": os.getenv("FASTMCP_SERVER_AUTH_JWT_REQUIRED_SCOPES", None),
}

DEFAULT_TRANSPORT = os.getenv("TRANSPORT", "stdio")
DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(string=os.getenv("PORT", "8000"))


def register_prompts(mcp: FastMCP):
    @mcp.prompt(name="find_recipe", description="Find a recipe in your cookbook.")
    def find_recipe(query: str) -> str:
        """Find a recipe."""
        return f"Please find the recipe '{query}'"

    @mcp.prompt(name="random_meal", description="Suggest a random meal.")
    def random_meal() -> str:
        """Suggest a random meal."""
        return "Please suggest a random meal."


def register_tools(mcp: FastMCP):
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check() -> Dict:
        return {"status": "OK"}

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"], tags={"app"}
    )
    async def get_startup_info(
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Startup Info"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_startup_info()

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"], tags={"app"}
    )
    async def get_app_theme(
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get App Theme"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_app_theme()

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def get_token(
        data: Dict = Field(default=None, description="Request body data"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Get Token"""
        if ctx:
            message = "Are you sure you want to POST /api/auth/token?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_token(data=data)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def oauth_login(
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Oauth Login"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.oauth_login()

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def oauth_callback(
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Oauth Callback"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.oauth_callback()

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def refresh_token(
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Refresh Token"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.refresh_token()

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def logout(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Logout"""
        if ctx:
            message = "Are you sure you want to POST /api/auth/logout?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.logout(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def register_new_user(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Register New User"""
        if ctx:
            message = "Are you sure you want to POST /api/users/register?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.register_new_user(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def get_logged_in_user(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Logged In User"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_logged_in_user(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def get_logged_in_user_ratings(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Logged In User Ratings"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_logged_in_user_ratings(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def get_logged_in_user_rating_for_recipe(
        recipe_id: str = Field(default=..., description="recipe_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Logged In User Rating For Recipe"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_logged_in_user_rating_for_recipe(
            recipe_id=recipe_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def get_logged_in_user_favorites(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Logged In User Favorites"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_logged_in_user_favorites(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def update_password(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update Password"""
        if ctx:
            message = "Are you sure you want to PUT /api/users/password?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.update_password(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def update_user(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update User"""
        if ctx:
            message = f"Are you sure you want to PUT /api/users/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.update_user(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def forgot_password(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Forgot Password"""
        if ctx:
            message = "Are you sure you want to POST /api/users/forgot-password?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.forgot_password(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def reset_password(
        data: Dict = Field(default=..., description="Request body data"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Reset Password"""
        if ctx:
            message = "Are you sure you want to POST /api/users/reset-password?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.reset_password(data=data)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def update_user_image(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update User Image"""
        if ctx:
            message = f"Are you sure you want to POST /api/users/{id}/image?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.update_user_image(
            id=id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def create(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create Api Token"""
        if ctx:
            message = "Are you sure you want to POST /api/users/api-tokens?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.create(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def delete(
        token_id: int = Field(default=..., description="token_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete Api Token"""
        if ctx:
            message = (
                f"Are you sure you want to DELETE /api/users/api-tokens/{token_id}?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete(token_id=token_id, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def get_ratings(
        id: str = Field(default=..., description="id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Ratings"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_ratings(id=id, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def get_favorites(
        id: str = Field(default=..., description="id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Favorites"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_favorites(id=id, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def set_rating(
        id: str = Field(default=..., description="id"),
        slug: str = Field(default=..., description="slug"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Set Rating"""
        if ctx:
            message = f"Are you sure you want to POST /api/users/{id}/ratings/{slug}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.set_rating(
            id=id, slug=slug, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def add_favorite(
        id: str = Field(default=..., description="id"),
        slug: str = Field(default=..., description="slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Add Favorite"""
        if ctx:
            message = f"Are you sure you want to POST /api/users/{id}/favorites/{slug}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.add_favorite(id=id, slug=slug, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"users"},
    )
    async def remove_favorite(
        id: str = Field(default=..., description="id"),
        slug: str = Field(default=..., description="slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Remove Favorite"""
        if ctx:
            message = (
                f"Are you sure you want to DELETE /api/users/{id}/favorites/{slug}?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.remove_favorite(id=id, slug=slug, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_households_cookbooks(
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_households_cookbooks(
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def post_households_cookbooks(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/households/cookbooks?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_households_cookbooks(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def put_households_cookbooks(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update Many"""
        if ctx:
            message = "Are you sure you want to PUT /api/households/cookbooks?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_households_cookbooks(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_households_cookbooks_item_id(
        item_id: Any = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_households_cookbooks_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def put_households_cookbooks_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = (
                f"Are you sure you want to PUT /api/households/cookbooks/{item_id}?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_households_cookbooks_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def delete_households_cookbooks_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = (
                f"Are you sure you want to DELETE /api/households/cookbooks/{item_id}?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_households_cookbooks_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_households_events_notifications(
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_households_events_notifications(
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def post_households_events_notifications(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = (
                "Are you sure you want to POST /api/households/events/notifications?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_households_events_notifications(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_households_events_notifications_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_households_events_notifications_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def put_households_events_notifications_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = f"Are you sure you want to PUT /api/households/events/notifications/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_households_events_notifications_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def delete_households_events_notifications_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/households/events/notifications/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_households_events_notifications_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def test_notification(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Test Notification"""
        if ctx:
            message = f"Are you sure you want to POST /api/households/events/notifications/{item_id}/test?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.test_notification(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_households_recipe_actions(
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_households_recipe_actions(
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def post_households_recipe_actions(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/households/recipe-actions?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_households_recipe_actions(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_households_recipe_actions_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_households_recipe_actions_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def put_households_recipe_actions_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = f"Are you sure you want to PUT /api/households/recipe-actions/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_households_recipe_actions_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def delete_households_recipe_actions_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/households/recipe-actions/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_households_recipe_actions_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def trigger_action(
        item_id: str = Field(default=..., description="item_id"),
        recipe_slug: str = Field(default=..., description="recipe_slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        data: Dict = Field(default=None, description="Request body data"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Trigger Action"""
        if ctx:
            message = f"Are you sure you want to POST /api/households/recipe-actions/{item_id}/trigger/{recipe_slug}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.trigger_action(
            item_id=item_id,
            recipe_slug=recipe_slug,
            accept_language=accept_language,
            data=data,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_logged_in_user_household(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Logged In User Household"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_logged_in_user_household(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_household_recipe(
        recipe_slug: str = Field(default=..., description="recipe_slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Household Recipe"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_household_recipe(
            recipe_slug=recipe_slug, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_household_members(
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Household Members"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_household_members(
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_household_preferences(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Household Preferences"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_household_preferences(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def update_household_preferences(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update Household Preferences"""
        if ctx:
            message = "Are you sure you want to PUT /api/households/preferences?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.update_household_preferences(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def set_member_permissions(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Set Member Permissions"""
        if ctx:
            message = "Are you sure you want to PUT /api/households/permissions?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.set_member_permissions(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_statistics(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Statistics"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_statistics(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_invite_tokens(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Invite Tokens"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_invite_tokens(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def create_invite_token(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create Invite Token"""
        if ctx:
            message = "Are you sure you want to POST /api/households/invitations?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.create_invite_token(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def email_invitation(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Email Invitation"""
        if ctx:
            message = "Are you sure you want to POST /api/households/invitations/email?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.email_invitation(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_households_shopping_lists(
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_households_shopping_lists(
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def post_households_shopping_lists(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/households/shopping/lists?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_households_shopping_lists(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_households_shopping_lists_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_households_shopping_lists_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def put_households_shopping_lists_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = f"Are you sure you want to PUT /api/households/shopping/lists/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_households_shopping_lists_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def delete_households_shopping_lists_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/households/shopping/lists/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_households_shopping_lists_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def update_label_settings(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update Label Settings"""
        if ctx:
            message = f"Are you sure you want to PUT /api/households/shopping/lists/{item_id}/label-settings?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.update_label_settings(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def add_recipe_ingredients_to_list(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Add Recipe Ingredients To List"""
        if ctx:
            message = f"Are you sure you want to POST /api/households/shopping/lists/{item_id}/recipe?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.add_recipe_ingredients_to_list(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def add_single_recipe_ingredients_to_list(
        item_id: str = Field(default=..., description="item_id"),
        recipe_id: str = Field(default=..., description="recipe_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        data: Dict = Field(default=None, description="Request body data"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Add Single Recipe Ingredients To List"""
        if ctx:
            message = f"Are you sure you want to POST /api/households/shopping/lists/{item_id}/recipe/{recipe_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.add_single_recipe_ingredients_to_list(
            item_id=item_id,
            recipe_id=recipe_id,
            accept_language=accept_language,
            data=data,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def remove_recipe_ingredients_from_list(
        item_id: str = Field(default=..., description="item_id"),
        recipe_id: str = Field(default=..., description="recipe_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        data: Dict = Field(default=None, description="Request body data"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Remove Recipe Ingredients From List"""
        if ctx:
            message = f"Are you sure you want to POST /api/households/shopping/lists/{item_id}/recipe/{recipe_id}/delete?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.remove_recipe_ingredients_from_list(
            item_id=item_id,
            recipe_id=recipe_id,
            accept_language=accept_language,
            data=data,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_households_shopping_items(
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_households_shopping_items(
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def post_households_shopping_items(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/households/shopping/items?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_households_shopping_items(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def put_households_shopping_items(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update Many"""
        if ctx:
            message = "Are you sure you want to PUT /api/households/shopping/items?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_households_shopping_items(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def delete_households_shopping_items(
        ids: List = Field(default=None, description="ids"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete Many"""
        if ctx:
            message = "Are you sure you want to DELETE /api/households/shopping/items?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_households_shopping_items(
            ids=ids, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def post_households_shopping_items_create_bulk(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create Many"""
        if ctx:
            message = "Are you sure you want to POST /api/households/shopping/items/create-bulk?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_households_shopping_items_create_bulk(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_households_shopping_items_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_households_shopping_items_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def put_households_shopping_items_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = f"Are you sure you want to PUT /api/households/shopping/items/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_households_shopping_items_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def delete_households_shopping_items_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/households/shopping/items/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_households_shopping_items_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_households_webhooks(
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_households_webhooks(
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def post_households_webhooks(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/households/webhooks?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_households_webhooks(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def rerun_webhooks(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Rerun Webhooks"""
        if ctx:
            message = "Are you sure you want to POST /api/households/webhooks/rerun?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.rerun_webhooks(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_households_webhooks_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_households_webhooks_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def put_households_webhooks_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = (
                f"Are you sure you want to PUT /api/households/webhooks/{item_id}?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_households_webhooks_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def delete_households_webhooks_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = (
                f"Are you sure you want to DELETE /api/households/webhooks/{item_id}?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_households_webhooks_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def test_one(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Test One"""
        if ctx:
            message = f"Are you sure you want to POST /api/households/webhooks/{item_id}/test?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.test_one(item_id=item_id, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_households_mealplans_rules(
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_households_mealplans_rules(
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def post_households_mealplans_rules(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/households/mealplans/rules?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_households_mealplans_rules(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_households_mealplans_rules_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_households_mealplans_rules_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def put_households_mealplans_rules_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = f"Are you sure you want to PUT /api/households/mealplans/rules/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_households_mealplans_rules_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def delete_households_mealplans_rules_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/households/mealplans/rules/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_households_mealplans_rules_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_households_mealplans(
        start_date: Any = Field(default=None, description="start_date"),
        end_date: Any = Field(default=None, description="end_date"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_households_mealplans(
            start_date=start_date,
            end_date=end_date,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def post_households_mealplans(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/households/mealplans?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_households_mealplans(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_todays_meals(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Todays Meals"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_todays_meals(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def create_random_meal(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create Random Meal"""
        if ctx:
            message = "Are you sure you want to POST /api/households/mealplans/random?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.create_random_meal(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def get_households_mealplans_item_id(
        item_id: int = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_households_mealplans_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def put_households_mealplans_item_id(
        item_id: int = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = (
                f"Are you sure you want to PUT /api/households/mealplans/{item_id}?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_households_mealplans_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"households"},
    )
    async def delete_households_mealplans_item_id(
        item_id: int = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = (
                f"Are you sure you want to DELETE /api/households/mealplans/{item_id}?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_households_mealplans_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def get_all_households(
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All Households"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_all_households(
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def get_one_household(
        household_slug: str = Field(default=..., description="household_slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One Household"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_one_household(
            household_slug=household_slug, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def get_logged_in_user_group(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Logged In User Group"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_logged_in_user_group(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def get_group_members(
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Group Members"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_group_members(
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def get_group_member(
        username_or_id: Any = Field(default=..., description="username_or_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Group Member"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_group_member(
            username_or_id=username_or_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def get_group_preferences(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Group Preferences"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_group_preferences(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def update_group_preferences(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update Group Preferences"""
        if ctx:
            message = "Are you sure you want to PUT /api/groups/preferences?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.update_group_preferences(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def get_storage(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Storage"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_storage(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def start_data_migration(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Start Data Migration"""
        if ctx:
            message = "Are you sure you want to POST /api/groups/migrations?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.start_data_migration(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def get_groups_reports(
        report_type: Any = Field(default=None, description="report_type"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_groups_reports(
            report_type=report_type, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def get_groups_reports_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_groups_reports_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def delete_groups_reports_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/groups/reports/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_groups_reports_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def get_groups_labels(
        search: Any = Field(default=None, description="search"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_groups_labels(
            search=search,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def post_groups_labels(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/groups/labels?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_groups_labels(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def get_groups_labels_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_groups_labels_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def put_groups_labels_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = f"Are you sure you want to PUT /api/groups/labels/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_groups_labels_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def delete_groups_labels_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/groups/labels/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_groups_labels_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def seed_foods(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Seed Foods"""
        if ctx:
            message = "Are you sure you want to POST /api/groups/seeders/foods?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.seed_foods(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def seed_labels(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Seed Labels"""
        if ctx:
            message = "Are you sure you want to POST /api/groups/seeders/labels?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.seed_labels(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"groups"},
    )
    async def seed_units(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Seed Units"""
        if ctx:
            message = "Are you sure you want to POST /api/groups/seeders/units?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.seed_units(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_recipe_formats_and_templates(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Recipe Formats And Templates"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_recipe_formats_and_templates(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_recipe_as_format(
        slug: str = Field(default=..., description="slug"),
        template_name: str = Field(default=..., description="template_name"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Recipe As Format"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_recipe_as_format(
            slug=slug, template_name=template_name, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def test_parse_recipe_url(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Test Parse Recipe Url"""
        if ctx:
            message = "Are you sure you want to POST /api/recipes/test-scrape-url?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.test_parse_recipe_url(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def create_recipe_from_html_or_json(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create Recipe From Html Or Json"""
        if ctx:
            message = "Are you sure you want to POST /api/recipes/create/html-or-json?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.create_recipe_from_html_or_json(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def parse_recipe_url(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Parse Recipe Url"""
        if ctx:
            message = "Are you sure you want to POST /api/recipes/create/url?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.parse_recipe_url(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def parse_recipe_url_bulk(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Parse Recipe Url Bulk"""
        if ctx:
            message = "Are you sure you want to POST /api/recipes/create/url/bulk?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.parse_recipe_url_bulk(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def create_recipe_from_zip(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create Recipe From Zip"""
        if ctx:
            message = "Are you sure you want to POST /api/recipes/create/zip?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.create_recipe_from_zip(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def create_recipe_from_image(
        data: Dict = Field(default=..., description="Request body data"),
        translate_language: Any = Field(default=None, description="translateLanguage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create Recipe From Image"""
        if ctx:
            message = "Are you sure you want to POST /api/recipes/create/image?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.create_recipe_from_image(
            data=data,
            translate_language=translate_language,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_recipes(
        categories: Any = Field(default=None, description="categories"),
        tags: Any = Field(default=None, description="tags"),
        tools: Any = Field(default=None, description="tools"),
        foods: Any = Field(default=None, description="foods"),
        households: Any = Field(default=None, description="households"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        cookbook: Any = Field(default=None, description="cookbook"),
        require_all_categories: bool = Field(
            default=None, description="requireAllCategories"
        ),
        require_all_tags: bool = Field(default=None, description="requireAllTags"),
        require_all_tools: bool = Field(default=None, description="requireAllTools"),
        require_all_foods: bool = Field(default=None, description="requireAllFoods"),
        search: Any = Field(default=None, description="search"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_recipes(
            categories=categories,
            tags=tags,
            tools=tools,
            foods=foods,
            households=households,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            cookbook=cookbook,
            require_all_categories=require_all_categories,
            require_all_tags=require_all_tags,
            require_all_tools=require_all_tools,
            require_all_foods=require_all_foods,
            search=search,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def post_recipes(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/recipes?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_recipes(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def put_recipes(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update Many"""
        if ctx:
            message = "Are you sure you want to PUT /api/recipes?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_recipes(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def patch_many(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Patch Many"""
        if ctx:
            message = "Are you sure you want to PATCH /api/recipes?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.patch_many(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_recipes_suggestions(
        foods: Any = Field(default=None, description="foods"),
        tools: Any = Field(default=None, description="tools"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        limit: int = Field(default=None, description="limit"),
        max_missing_foods: int = Field(default=None, description="maxMissingFoods"),
        max_missing_tools: int = Field(default=None, description="maxMissingTools"),
        include_foods_on_hand: bool = Field(
            default=None, description="includeFoodsOnHand"
        ),
        include_tools_on_hand: bool = Field(
            default=None, description="includeToolsOnHand"
        ),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Suggest Recipes"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_recipes_suggestions(
            foods=foods,
            tools=tools,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            limit=limit,
            max_missing_foods=max_missing_foods,
            max_missing_tools=max_missing_tools,
            include_foods_on_hand=include_foods_on_hand,
            include_tools_on_hand=include_tools_on_hand,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_recipes_slug(
        slug: str = Field(default=..., description="A recipe's slug or id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_recipes_slug(slug=slug, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def put_recipes_slug(
        slug: str = Field(default=..., description="slug"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = f"Are you sure you want to PUT /api/recipes/{slug}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_recipes_slug(
            slug=slug, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def patch_one(
        slug: str = Field(default=..., description="slug"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Patch One"""
        if ctx:
            message = f"Are you sure you want to PATCH /api/recipes/{slug}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.patch_one(slug=slug, data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def delete_recipes_slug(
        slug: str = Field(default=..., description="slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/recipes/{slug}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_recipes_slug(slug=slug, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def duplicate_one(
        slug: str = Field(default=..., description="slug"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Duplicate One"""
        if ctx:
            message = f"Are you sure you want to POST /api/recipes/{slug}/duplicate?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.duplicate_one(
            slug=slug, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def update_last_made(
        slug: str = Field(default=..., description="slug"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update Last Made"""
        if ctx:
            message = f"Are you sure you want to PATCH /api/recipes/{slug}/last-made?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.update_last_made(
            slug=slug, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def scrape_image_url(
        slug: str = Field(default=..., description="slug"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Scrape Image Url"""
        if ctx:
            message = f"Are you sure you want to POST /api/recipes/{slug}/image?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.scrape_image_url(
            slug=slug, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def update_recipe_image(
        slug: str = Field(default=..., description="slug"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update Recipe Image"""
        if ctx:
            message = f"Are you sure you want to PUT /api/recipes/{slug}/image?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.update_recipe_image(
            slug=slug, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def delete_recipe_image(
        slug: str = Field(default=..., description="slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete Recipe Image"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/recipes/{slug}/image?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_recipe_image(slug=slug, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def upload_recipe_asset(
        slug: str = Field(default=..., description="slug"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Upload Recipe Asset"""
        if ctx:
            message = f"Are you sure you want to POST /api/recipes/{slug}/assets?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.upload_recipe_asset(
            slug=slug, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_recipe_comments(
        slug: str = Field(default=..., description="slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Recipe Comments"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_recipe_comments(slug=slug, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def bulk_tag_recipes(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Bulk Tag Recipes"""
        if ctx:
            message = "Are you sure you want to POST /api/recipes/bulk-actions/tag?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.bulk_tag_recipes(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def bulk_settings_recipes(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Bulk Settings Recipes"""
        if ctx:
            message = (
                "Are you sure you want to POST /api/recipes/bulk-actions/settings?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.bulk_settings_recipes(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def bulk_categorize_recipes(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Bulk Categorize Recipes"""
        if ctx:
            message = (
                "Are you sure you want to POST /api/recipes/bulk-actions/categorize?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.bulk_categorize_recipes(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def bulk_delete_recipes(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Bulk Delete Recipes"""
        if ctx:
            message = "Are you sure you want to POST /api/recipes/bulk-actions/delete?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.bulk_delete_recipes(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def bulk_export_recipes(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Bulk Export Recipes"""
        if ctx:
            message = "Are you sure you want to POST /api/recipes/bulk-actions/export?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.bulk_export_recipes(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_exported_data(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Exported Data"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_exported_data(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_exported_data_token(
        export_id: str = Field(default=..., description="export_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Exported Data Token"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_exported_data_token(
            export_id=export_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def purge_export_data(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Purge Export Data"""
        if ctx:
            message = "Are you sure you want to DELETE /api/recipes/bulk-actions/export/purge?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.purge_export_data(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_shared_recipe(
        token_id: str = Field(default=..., description="token_id"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Shared Recipe"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_shared_recipe(token_id=token_id)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_shared_recipe_as_zip(
        token_id: str = Field(default=..., description="token_id"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Shared Recipe As Zip"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_shared_recipe_as_zip(token_id=token_id)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_recipes_timeline_events(
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_recipes_timeline_events(
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def post_recipes_timeline_events(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/recipes/timeline/events?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_recipes_timeline_events(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_recipes_timeline_events_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_recipes_timeline_events_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def put_recipes_timeline_events_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = (
                f"Are you sure you want to PUT /api/recipes/timeline/events/{item_id}?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_recipes_timeline_events_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def delete_recipes_timeline_events_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/recipes/timeline/events/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_recipes_timeline_events_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def update_event_image(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update Event Image"""
        if ctx:
            message = f"Are you sure you want to PUT /api/recipes/timeline/events/{item_id}/image?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.update_event_image(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def get_organizers_categories(
        search: Any = Field(default=None, description="search"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_organizers_categories(
            search=search,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def post_organizers_categories(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/organizers/categories?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_organizers_categories(
            data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def get_all_empty(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All Empty"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_all_empty(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def get_organizers_categories_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_organizers_categories_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def put_organizers_categories_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = (
                f"Are you sure you want to PUT /api/organizers/categories/{item_id}?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_organizers_categories_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def delete_organizers_categories_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = (
                f"Are you sure you want to DELETE /api/organizers/categories/{item_id}?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_organizers_categories_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def get_organizers_categories_slug_category_slug(
        category_slug: str = Field(default=..., description="category_slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One By Slug"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_organizers_categories_slug_category_slug(
            category_slug=category_slug, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def get_organizers_tags(
        search: Any = Field(default=None, description="search"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_organizers_tags(
            search=search,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def post_organizers_tags(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/organizers/tags?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_organizers_tags(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def get_empty_tags(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Empty Tags"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_empty_tags(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def get_organizers_tags_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_organizers_tags_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def put_organizers_tags_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = f"Are you sure you want to PUT /api/organizers/tags/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_organizers_tags_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def delete_recipe_tag(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete Recipe Tag"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/organizers/tags/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_recipe_tag(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def get_organizers_tags_slug_tag_slug(
        tag_slug: str = Field(default=..., description="tag_slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One By Slug"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_organizers_tags_slug_tag_slug(
            tag_slug=tag_slug, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def get_organizers_tools(
        search: Any = Field(default=None, description="search"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_organizers_tools(
            search=search,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def post_organizers_tools(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/organizers/tools?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_organizers_tools(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def get_organizers_tools_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_organizers_tools_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def put_organizers_tools_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = f"Are you sure you want to PUT /api/organizers/tools/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_organizers_tools_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def delete_organizers_tools_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = (
                f"Are you sure you want to DELETE /api/organizers/tools/{item_id}?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_organizers_tools_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"organizer"},
    )
    async def get_organizers_tools_slug_tool_slug(
        tool_slug: str = Field(default=..., description="tool_slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One By Slug"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_organizers_tools_slug_tool_slug(
            tool_slug=tool_slug, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"shared"},
    )
    async def get_shared_recipes(
        recipe_id: Any = Field(default=None, description="recipe_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_shared_recipes(
            recipe_id=recipe_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"shared"},
    )
    async def post_shared_recipes(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/shared/recipes?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_shared_recipes(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"shared"},
    )
    async def get_shared_recipes_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_shared_recipes_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"shared"},
    )
    async def delete_shared_recipes_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/shared/recipes/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_shared_recipes_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_comments(
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_comments(
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def post_comments(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/comments?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_comments(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_comments_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_comments_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def put_comments_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = f"Are you sure you want to PUT /api/comments/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_comments_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def post_parser_ingredient(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/comments/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_parser_ingredient(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def parse_ingredient(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Parse Ingredient"""
        if ctx:
            message = "Are you sure you want to POST /api/parser/ingredient?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.parse_ingredient(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def parse_ingredients(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Parse Ingredients"""
        if ctx:
            message = "Are you sure you want to POST /api/parser/ingredients?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.parse_ingredients(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipes"},
    )
    async def get_foods(
        search: Any = Field(default=None, description="search"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_foods(
            search=search,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipes"},
    )
    async def post_foods(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/foods?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_foods(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipes"},
    )
    async def put_foods_merge(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Merge One"""
        if ctx:
            message = "Are you sure you want to PUT /api/foods/merge?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_foods_merge(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipes"},
    )
    async def get_foods_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_foods_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipes"},
    )
    async def put_foods_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = f"Are you sure you want to PUT /api/foods/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_foods_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipes"},
    )
    async def delete_foods_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/foods/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_foods_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipes"},
    )
    async def get_units(
        search: Any = Field(default=None, description="search"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_units(
            search=search,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipes"},
    )
    async def post_units(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/units?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_units(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipes"},
    )
    async def put_units_merge(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Merge One"""
        if ctx:
            message = "Are you sure you want to PUT /api/units/merge?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_units_merge(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipes"},
    )
    async def get_units_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_units_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipes"},
    )
    async def put_units_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = f"Are you sure you want to PUT /api/units/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_units_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipes"},
    )
    async def delete_units_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/units/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_units_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def get_app_info(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get App Info"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_app_info(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def get_app_statistics(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get App Statistics"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_app_statistics(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def check_app_config(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Check App Config"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.check_app_config(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def get_admin_users(
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_admin_users(
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def post_admin_users(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/admin/users?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_admin_users(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def unlock_users(
        force: bool = Field(default=None, description="force"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Unlock Users"""
        if ctx:
            message = "Are you sure you want to POST /api/admin/users/unlock?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.unlock_users(force=force, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def get_admin_users_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_admin_users_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def put_admin_users_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = f"Are you sure you want to PUT /api/admin/users/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_admin_users_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def delete_admin_users_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/admin/users/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_admin_users_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def generate_token(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Generate Token"""
        if ctx:
            message = (
                "Are you sure you want to POST /api/admin/users/password-reset-token?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.generate_token(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def get_admin_households(
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_admin_households(
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def post_admin_households(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/admin/households?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_admin_households(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def get_admin_households_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_admin_households_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def put_admin_households_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = f"Are you sure you want to PUT /api/admin/households/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_admin_households_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def delete_admin_households_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = (
                f"Are you sure you want to DELETE /api/admin/households/{item_id}?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_admin_households_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def get_admin_groups(
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_admin_groups(
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def post_admin_groups(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/admin/groups?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_admin_groups(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def get_admin_groups_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_admin_groups_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def put_admin_groups_item_id(
        item_id: str = Field(default=..., description="item_id"),
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Update One"""
        if ctx:
            message = f"Are you sure you want to PUT /api/admin/groups/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.put_admin_groups_item_id(
            item_id=item_id, data=data, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def delete_admin_groups_item_id(
        item_id: str = Field(default=..., description="item_id"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/admin/groups/{item_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_admin_groups_item_id(
            item_id=item_id, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def check_email_config(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Check Email Config"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.check_email_config(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def send_test_email(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Send Test Email"""
        if ctx:
            message = "Are you sure you want to POST /api/admin/email?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.send_test_email(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def get_admin_backups(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_admin_backups(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def post_admin_backups(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Create One"""
        if ctx:
            message = "Are you sure you want to POST /api/admin/backups?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.post_admin_backups(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def get_admin_backups_file_name(
        file_name: str = Field(default=..., description="file_name"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_admin_backups_file_name(
            file_name=file_name, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def delete_admin_backups_file_name(
        file_name: str = Field(default=..., description="file_name"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Delete One"""
        if ctx:
            message = f"Are you sure you want to DELETE /api/admin/backups/{file_name}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.delete_admin_backups_file_name(
            file_name=file_name, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def upload_one(
        data: Dict = Field(default=..., description="Request body data"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Upload One"""
        if ctx:
            message = "Are you sure you want to POST /api/admin/backups/upload?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.upload_one(data=data, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def import_one(
        file_name: str = Field(default=..., description="file_name"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Import One"""
        if ctx:
            message = (
                f"Are you sure you want to POST /api/admin/backups/{file_name}/restore?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.import_one(file_name=file_name, accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def get_maintenance_summary(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Maintenance Summary"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_maintenance_summary(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def get_storage_details(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Storage Details"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_storage_details(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def clean_images(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Clean Images"""
        if ctx:
            message = (
                "Are you sure you want to POST /api/admin/maintenance/clean/images?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.clean_images(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def clean_temp(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Clean Temp"""
        if ctx:
            message = "Are you sure you want to POST /api/admin/maintenance/clean/temp?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.clean_temp(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def clean_recipe_folders(
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Clean Recipe Folders"""
        if ctx:
            message = "Are you sure you want to POST /api/admin/maintenance/clean/recipe-folders?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.clean_recipe_folders(accept_language=accept_language)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"admin"},
    )
    async def debug_openai(
        accept_language: Any = Field(default=None, description="accept-language"),
        data: Dict = Field(default=None, description="Request body data"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
        ctx: Context = None,
    ) -> Dict:
        """Debug Openai"""
        if ctx:
            message = "Are you sure you want to POST /api/admin/debug/openai?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {"status": "cancelled", "message": "User cancelled"}
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.debug_openai(accept_language=accept_language, data=data)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"explore"},
    )
    async def get_explore_groups_group_slug_foods(
        group_slug: str = Field(default=..., description="group_slug"),
        search: Any = Field(default=None, description="search"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_explore_groups_group_slug_foods(
            group_slug=group_slug,
            search=search,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"explore"},
    )
    async def get_explore_groups_group_slug_foods_item_id(
        item_id: str = Field(default=..., description="item_id"),
        group_slug: str = Field(default=..., description="group_slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_explore_groups_group_slug_foods_item_id(
            item_id=item_id, group_slug=group_slug, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"explore"},
    )
    async def get_explore_groups_group_slug_households(
        group_slug: str = Field(default=..., description="group_slug"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_explore_groups_group_slug_households(
            group_slug=group_slug,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"explore"},
    )
    async def get_household(
        household_slug: str = Field(default=..., description="household_slug"),
        group_slug: str = Field(default=..., description="group_slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Household"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_household(
            household_slug=household_slug,
            group_slug=group_slug,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"explore"},
    )
    async def get_explore_groups_group_slug_organizers_categories(
        group_slug: str = Field(default=..., description="group_slug"),
        search: Any = Field(default=None, description="search"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_explore_groups_group_slug_organizers_categories(
            group_slug=group_slug,
            search=search,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"explore"},
    )
    async def get_explore_groups_group_slug_organizers_categories_item_id(
        item_id: str = Field(default=..., description="item_id"),
        group_slug: str = Field(default=..., description="group_slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_explore_groups_group_slug_organizers_categories_item_id(
            item_id=item_id, group_slug=group_slug, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"explore"},
    )
    async def get_explore_groups_group_slug_organizers_tags(
        group_slug: str = Field(default=..., description="group_slug"),
        search: Any = Field(default=None, description="search"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_explore_groups_group_slug_organizers_tags(
            group_slug=group_slug,
            search=search,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"explore"},
    )
    async def get_explore_groups_group_slug_organizers_tags_item_id(
        item_id: str = Field(default=..., description="item_id"),
        group_slug: str = Field(default=..., description="group_slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_explore_groups_group_slug_organizers_tags_item_id(
            item_id=item_id, group_slug=group_slug, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"explore"},
    )
    async def get_explore_groups_group_slug_organizers_tools(
        group_slug: str = Field(default=..., description="group_slug"),
        search: Any = Field(default=None, description="search"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_explore_groups_group_slug_organizers_tools(
            group_slug=group_slug,
            search=search,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"explore"},
    )
    async def get_explore_groups_group_slug_organizers_tools_item_id(
        item_id: str = Field(default=..., description="item_id"),
        group_slug: str = Field(default=..., description="group_slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_explore_groups_group_slug_organizers_tools_item_id(
            item_id=item_id, group_slug=group_slug, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"explore"},
    )
    async def get_explore_groups_group_slug_cookbooks(
        group_slug: str = Field(default=..., description="group_slug"),
        search: Any = Field(default=None, description="search"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_explore_groups_group_slug_cookbooks(
            group_slug=group_slug,
            search=search,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"explore"},
    )
    async def get_explore_groups_group_slug_cookbooks_item_id(
        item_id: Any = Field(default=..., description="item_id"),
        group_slug: str = Field(default=..., description="group_slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get One"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_explore_groups_group_slug_cookbooks_item_id(
            item_id=item_id, group_slug=group_slug, accept_language=accept_language
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"explore"},
    )
    async def get_explore_groups_group_slug_recipes(
        group_slug: str = Field(default=..., description="group_slug"),
        categories: Any = Field(default=None, description="categories"),
        tags: Any = Field(default=None, description="tags"),
        tools: Any = Field(default=None, description="tools"),
        foods: Any = Field(default=None, description="foods"),
        households: Any = Field(default=None, description="households"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        page: int = Field(default=None, description="page"),
        per_page: int = Field(default=None, description="perPage"),
        cookbook: Any = Field(default=None, description="cookbook"),
        require_all_categories: bool = Field(
            default=None, description="requireAllCategories"
        ),
        require_all_tags: bool = Field(default=None, description="requireAllTags"),
        require_all_tools: bool = Field(default=None, description="requireAllTools"),
        require_all_foods: bool = Field(default=None, description="requireAllFoods"),
        search: Any = Field(default=None, description="search"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get All"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_explore_groups_group_slug_recipes(
            group_slug=group_slug,
            categories=categories,
            tags=tags,
            tools=tools,
            foods=foods,
            households=households,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            cookbook=cookbook,
            require_all_categories=require_all_categories,
            require_all_tags=require_all_tags,
            require_all_tools=require_all_tools,
            require_all_foods=require_all_foods,
            search=search,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"explore"},
    )
    async def get_explore_groups_group_slug_recipes_suggestions(
        group_slug: str = Field(default=..., description="group_slug"),
        foods: Any = Field(default=None, description="foods"),
        tools: Any = Field(default=None, description="tools"),
        order_by: Any = Field(default=None, description="orderBy"),
        order_by_null_position: Any = Field(
            default=None, description="orderByNullPosition"
        ),
        order_direction: Any = Field(default=None, description="orderDirection"),
        query_filter: Any = Field(default=None, description="queryFilter"),
        pagination_seed: Any = Field(default=None, description="paginationSeed"),
        limit: int = Field(default=None, description="limit"),
        max_missing_foods: int = Field(default=None, description="maxMissingFoods"),
        max_missing_tools: int = Field(default=None, description="maxMissingTools"),
        include_foods_on_hand: bool = Field(
            default=None, description="includeFoodsOnHand"
        ),
        include_tools_on_hand: bool = Field(
            default=None, description="includeToolsOnHand"
        ),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Suggest Recipes"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_explore_groups_group_slug_recipes_suggestions(
            group_slug=group_slug,
            foods=foods,
            tools=tools,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            limit=limit,
            max_missing_foods=max_missing_foods,
            max_missing_tools=max_missing_tools,
            include_foods_on_hand=include_foods_on_hand,
            include_tools_on_hand=include_tools_on_hand,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"explore"},
    )
    async def get_recipe(
        recipe_slug: str = Field(default=..., description="recipe_slug"),
        group_slug: str = Field(default=..., description="group_slug"),
        accept_language: Any = Field(default=None, description="accept-language"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Recipe"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_recipe(
            recipe_slug=recipe_slug,
            group_slug=group_slug,
            accept_language=accept_language,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_recipe_img(
        recipe_id: str = Field(default=..., description="recipe_id"),
        file_name: Any = Field(default=..., description="file_name"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Recipe Img"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_recipe_img(recipe_id=recipe_id, file_name=file_name)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_recipe_timeline_event_img(
        recipe_id: str = Field(default=..., description="recipe_id"),
        timeline_event_id: str = Field(default=..., description="timeline_event_id"),
        file_name: Any = Field(default=..., description="file_name"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Recipe Timeline Event Img"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_recipe_timeline_event_img(
            recipe_id=recipe_id,
            timeline_event_id=timeline_event_id,
            file_name=file_name,
        )

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_recipe_asset(
        recipe_id: str = Field(default=..., description="recipe_id"),
        file_name: str = Field(default=..., description="file_name"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Recipe Asset"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_recipe_asset(recipe_id=recipe_id, file_name=file_name)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_user_image(
        user_id: str = Field(default=..., description="user_id"),
        file_name: str = Field(default=..., description="file_name"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get User Image"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_user_image(user_id=user_id, file_name=file_name)

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipe"},
    )
    async def get_validation_text(
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Validation Text"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.get_validation_text()

    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"utils"},
    )
    async def download_file(
        token: Any = Field(default=None, description="token"),
        mealie_base_url: str = Field(
            default=os.environ.get("MEALIE_BASE_URL", None),
            description="Mealie Base URL",
        ),
        mealie_token: Optional[str] = Field(
            default=os.environ.get("MEALIE_TOKEN", None), description="API Token"
        ),
        mealie_verify: bool = Field(
            default=to_boolean(os.environ.get("MEALIE_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Download File"""
        client = Api(base_url=mealie_base_url, token=mealie_token, verify=mealie_verify)
        return client.download_file(token=token)


def mealie_mcp() -> None:
    """Run the Mealie MCP server with specified transport and connection parameters.

    This function parses command-line arguments to configure and start the MCP server for Mealie API interactions.
    It supports stdio or TCP transport modes and exits on invalid arguments or help requests.

    """
    parser = argparse.ArgumentParser(add_help=False, description="Mealie MCP Server")
    parser.add_argument(
        "-t",
        "--transport",
        default=DEFAULT_TRANSPORT,
        choices=["stdio", "streamable-http", "sse"],
        help="Transport method: 'stdio', 'streamable-http', or 'sse' [legacy] (default: stdio)",
    )
    parser.add_argument(
        "-s",
        "--host",
        default=DEFAULT_HOST,
        help="Host address for HTTP transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Port number for HTTP transport (default: 8000)",
    )
    parser.add_argument(
        "--auth-type",
        default="none",
        choices=["none", "static", "jwt", "oauth-proxy", "oidc-proxy", "remote-oauth"],
        help="Authentication type for MCP server: 'none' (disabled), 'static' (internal), 'jwt' (external token verification), 'oauth-proxy', 'oidc-proxy', 'remote-oauth' (external) (default: none)",
    )
    parser.add_argument(
        "--token-jwks-uri", default=None, help="JWKS URI for JWT verification"
    )
    parser.add_argument(
        "--token-issuer", default=None, help="Issuer for JWT verification"
    )
    parser.add_argument(
        "--token-audience", default=None, help="Audience for JWT verification"
    )
    parser.add_argument(
        "--token-algorithm",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_ALGORITHM"),
        choices=[
            "HS256",
            "HS384",
            "HS512",
            "RS256",
            "RS384",
            "RS512",
            "ES256",
            "ES384",
            "ES512",
        ],
        help="JWT signing algorithm (required for HMAC or static key). Auto-detected for JWKS.",
    )
    parser.add_argument(
        "--token-secret",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY"),
        help="Shared secret for HMAC (HS*) or PEM public key for static asymmetric verification.",
    )
    parser.add_argument(
        "--token-public-key",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY"),
        help="Path to PEM public key file or inline PEM string (for static asymmetric keys).",
    )
    parser.add_argument(
        "--required-scopes",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_REQUIRED_SCOPES"),
        help="Comma-separated list of required scopes (e.g., mealie.read,mealie.write).",
    )
    parser.add_argument(
        "--oauth-upstream-auth-endpoint",
        default=None,
        help="Upstream authorization endpoint for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-token-endpoint",
        default=None,
        help="Upstream token endpoint for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-client-id",
        default=None,
        help="Upstream client ID for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-client-secret",
        default=None,
        help="Upstream client secret for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-base-url", default=None, help="Base URL for OAuth Proxy"
    )
    parser.add_argument(
        "--oidc-config-url", default=None, help="OIDC configuration URL"
    )
    parser.add_argument("--oidc-client-id", default=None, help="OIDC client ID")
    parser.add_argument("--oidc-client-secret", default=None, help="OIDC client secret")
    parser.add_argument("--oidc-base-url", default=None, help="Base URL for OIDC Proxy")
    parser.add_argument(
        "--remote-auth-servers",
        default=None,
        help="Comma-separated list of authorization servers for Remote OAuth",
    )
    parser.add_argument(
        "--remote-base-url", default=None, help="Base URL for Remote OAuth"
    )
    parser.add_argument(
        "--allowed-client-redirect-uris",
        default=None,
        help="Comma-separated list of allowed client redirect URIs",
    )
    parser.add_argument(
        "--eunomia-type",
        default="none",
        choices=["none", "embedded", "remote"],
        help="Eunomia authorization type: 'none' (disabled), 'embedded' (built-in), 'remote' (external) (default: none)",
    )
    parser.add_argument(
        "--eunomia-policy-file",
        default="mcp_policies.json",
        help="Policy file for embedded Eunomia (default: mcp_policies.json)",
    )
    parser.add_argument(
        "--eunomia-remote-url", default=None, help="URL for remote Eunomia server"
    )
    parser.add_argument(
        "--enable-delegation",
        action="store_true",
        default=to_boolean(os.environ.get("ENABLE_DELEGATION", "False")),
        help="Enable OIDC token delegation",
    )
    parser.add_argument(
        "--audience",
        default=os.environ.get("AUDIENCE", None),
        help="Audience for the delegated token",
    )
    parser.add_argument(
        "--delegated-scopes",
        default=os.environ.get("DELEGATED_SCOPES", "api"),
        help="Scopes for the delegated token (space-separated)",
    )
    parser.add_argument(
        "--openapi-file",
        default=None,
        help="Path to the OpenAPI JSON file to import additional tools from",
    )
    parser.add_argument(
        "--openapi-base-url",
        default=None,
        help="Base URL for the OpenAPI client (overrides instance URL)",
    )
    parser.add_argument(
        "--openapi-use-token",
        action="store_true",
        help="Use the incoming Bearer token (from MCP request) to authenticate OpenAPI import",
    )

    parser.add_argument(
        "--openapi-username",
        default=os.getenv("OPENAPI_USERNAME"),
        help="Username for basic auth during OpenAPI import",
    )

    parser.add_argument(
        "--openapi-password",
        default=os.getenv("OPENAPI_PASSWORD"),
        help="Password for basic auth during OpenAPI import",
    )

    parser.add_argument(
        "--openapi-client-id",
        default=os.getenv("OPENAPI_CLIENT_ID"),
        help="OAuth client ID for OpenAPI import",
    )

    parser.add_argument(
        "--openapi-client-secret",
        default=os.getenv("OPENAPI_CLIENT_SECRET"),
        help="OAuth client secret for OpenAPI import",
    )

    parser.add_argument("--help", action="store_true", help="Show usage")

    args = parser.parse_args()

    if hasattr(args, "help") and args.help:

        parser.print_help()

        sys.exit(0)

    if args.port < 0 or args.port > 65535:
        print(f"Error: Port {args.port} is out of valid range (0-65535).")
        sys.exit(1)

    config["enable_delegation"] = args.enable_delegation
    config["audience"] = args.audience or config["audience"]
    config["delegated_scopes"] = args.delegated_scopes or config["delegated_scopes"]
    config["oidc_config_url"] = args.oidc_config_url or config["oidc_config_url"]
    config["oidc_client_id"] = args.oidc_client_id or config["oidc_client_id"]
    config["oidc_client_secret"] = (
        args.oidc_client_secret or config["oidc_client_secret"]
    )

    if config["enable_delegation"]:
        if args.auth_type != "oidc-proxy":
            logger.error("Token delegation requires auth-type=oidc-proxy")
            sys.exit(1)
        if not config["audience"]:
            logger.error("audience is required for delegation")
            sys.exit(1)
        if not all(
            [
                config["oidc_config_url"],
                config["oidc_client_id"],
                config["oidc_client_secret"],
            ]
        ):
            logger.error(
                "Delegation requires complete OIDC configuration (oidc-config-url, oidc-client-id, oidc-client-secret)"
            )
            sys.exit(1)

        try:
            logger.info(
                "Fetching OIDC configuration",
                extra={"oidc_config_url": config["oidc_config_url"]},
            )
            oidc_config_resp = requests.get(config["oidc_config_url"])
            oidc_config_resp.raise_for_status()
            oidc_config = oidc_config_resp.json()
            config["token_endpoint"] = oidc_config.get("token_endpoint")
            if not config["token_endpoint"]:
                logger.error("No token_endpoint found in OIDC configuration")
                raise ValueError("No token_endpoint found in OIDC configuration")
            logger.info(
                "OIDC configuration fetched successfully",
                extra={"token_endpoint": config["token_endpoint"]},
            )
        except Exception as e:
            print(f"Failed to fetch OIDC configuration: {e}")
            logger.error(
                "Failed to fetch OIDC configuration",
                extra={"error_type": type(e).__name__, "error_message": str(e)},
            )
            sys.exit(1)

    auth = None
    allowed_uris = (
        args.allowed_client_redirect_uris.split(",")
        if args.allowed_client_redirect_uris
        else None
    )

    if args.auth_type == "none":
        auth = None
    elif args.auth_type == "static":
        auth = StaticTokenVerifier(
            tokens={
                "test-token": {"client_id": "test-user", "scopes": ["read", "write"]},
                "admin-token": {"client_id": "admin", "scopes": ["admin"]},
            }
        )
    elif args.auth_type == "jwt":
        jwks_uri = args.token_jwks_uri or os.getenv("FASTMCP_SERVER_AUTH_JWT_JWKS_URI")
        issuer = args.token_issuer or os.getenv("FASTMCP_SERVER_AUTH_JWT_ISSUER")
        audience = args.token_audience or os.getenv("FASTMCP_SERVER_AUTH_JWT_AUDIENCE")
        algorithm = args.token_algorithm
        secret_or_key = args.token_secret or args.token_public_key
        public_key_pem = None

        if not (jwks_uri or secret_or_key):
            logger.error(
                "JWT auth requires either --token-jwks-uri or --token-secret/--token-public-key"
            )
            sys.exit(1)
        if not (issuer and audience):
            logger.error("JWT requires --token-issuer and --token-audience")
            sys.exit(1)

        if args.token_public_key and os.path.isfile(args.token_public_key):
            try:
                with open(args.token_public_key, "r") as f:
                    public_key_pem = f.read()
                logger.info(f"Loaded static public key from {args.token_public_key}")
            except Exception as e:
                print(f"Failed to read public key file: {e}")
                logger.error(f"Failed to read public key file: {e}")
                sys.exit(1)
        elif args.token_public_key:
            public_key_pem = args.token_public_key

        if jwks_uri and (algorithm or secret_or_key):
            logger.warning(
                "JWKS mode ignores --token-algorithm and --token-secret/--token-public-key"
            )

        if algorithm and algorithm.startswith("HS"):
            if not secret_or_key:
                logger.error(f"HMAC algorithm {algorithm} requires --token-secret")
                sys.exit(1)
            if jwks_uri:
                logger.error("Cannot use --token-jwks-uri with HMAC")
                sys.exit(1)
            public_key = secret_or_key
        else:
            public_key = public_key_pem

        required_scopes = None
        if args.required_scopes:
            required_scopes = [
                s.strip() for s in args.required_scopes.split(",") if s.strip()
            ]

        try:
            auth = JWTVerifier(
                jwks_uri=jwks_uri,
                public_key=public_key,
                issuer=issuer,
                audience=audience,
                algorithm=(
                    algorithm if algorithm and algorithm.startswith("HS") else None
                ),
                required_scopes=required_scopes,
            )
            logger.info(
                "JWTVerifier configured",
                extra={
                    "mode": (
                        "JWKS"
                        if jwks_uri
                        else (
                            "HMAC"
                            if algorithm and algorithm.startswith("HS")
                            else "Static Key"
                        )
                    ),
                    "algorithm": algorithm,
                    "required_scopes": required_scopes,
                },
            )
        except Exception as e:
            print(f"Failed to initialize JWTVerifier: {e}")
            logger.error(f"Failed to initialize JWTVerifier: {e}")
            sys.exit(1)
    elif args.auth_type == "oauth-proxy":
        if not (
            args.oauth_upstream_auth_endpoint
            and args.oauth_upstream_token_endpoint
            and args.oauth_upstream_client_id
            and args.oauth_upstream_client_secret
            and args.oauth_base_url
            and args.token_jwks_uri
            and args.token_issuer
            and args.token_audience
        ):
            print(
                "oauth-proxy requires oauth-upstream-auth-endpoint, oauth-upstream-token-endpoint, "
                "oauth-upstream-client-id, oauth-upstream-client-secret, oauth-base-url, token-jwks-uri, "
                "token-issuer, token-audience"
            )
            logger.error(
                "oauth-proxy requires oauth-upstream-auth-endpoint, oauth-upstream-token-endpoint, "
                "oauth-upstream-client-id, oauth-upstream-client-secret, oauth-base-url, token-jwks-uri, "
                "token-issuer, token-audience",
                extra={
                    "auth_endpoint": args.oauth_upstream_auth_endpoint,
                    "token_endpoint": args.oauth_upstream_token_endpoint,
                    "client_id": args.oauth_upstream_client_id,
                    "base_url": args.oauth_base_url,
                    "jwks_uri": args.token_jwks_uri,
                    "issuer": args.token_issuer,
                    "audience": args.token_audience,
                },
            )
            sys.exit(1)
        token_verifier = JWTVerifier(
            jwks_uri=args.token_jwks_uri,
            issuer=args.token_issuer,
            audience=args.token_audience,
        )
        auth = OAuthProxy(
            upstream_authorization_endpoint=args.oauth_upstream_auth_endpoint,
            upstream_token_endpoint=args.oauth_upstream_token_endpoint,
            upstream_client_id=args.oauth_upstream_client_id,
            upstream_client_secret=args.oauth_upstream_client_secret,
            token_verifier=token_verifier,
            base_url=args.oauth_base_url,
            allowed_client_redirect_uris=allowed_uris,
        )
    elif args.auth_type == "oidc-proxy":
        if not (
            args.oidc_config_url
            and args.oidc_client_id
            and args.oidc_client_secret
            and args.oidc_base_url
        ):
            logger.error(
                "oidc-proxy requires oidc-config-url, oidc-client-id, oidc-client-secret, oidc-base-url",
                extra={
                    "config_url": args.oidc_config_url,
                    "client_id": args.oidc_client_id,
                    "base_url": args.oidc_base_url,
                },
            )
            sys.exit(1)
        auth = OIDCProxy(
            config_url=args.oidc_config_url,
            client_id=args.oidc_client_id,
            client_secret=args.oidc_client_secret,
            base_url=args.oidc_base_url,
            allowed_client_redirect_uris=allowed_uris,
        )
    elif args.auth_type == "remote-oauth":
        if not (
            args.remote_auth_servers
            and args.remote_base_url
            and args.token_jwks_uri
            and args.token_issuer
            and args.token_audience
        ):
            logger.error(
                "remote-oauth requires remote-auth-servers, remote-base-url, token-jwks-uri, token-issuer, token-audience",
                extra={
                    "auth_servers": args.remote_auth_servers,
                    "base_url": args.remote_base_url,
                    "jwks_uri": args.token_jwks_uri,
                    "issuer": args.token_issuer,
                    "audience": args.token_audience,
                },
            )
            sys.exit(1)
        auth_servers = [url.strip() for url in args.remote_auth_servers.split(",")]
        token_verifier = JWTVerifier(
            jwks_uri=args.token_jwks_uri,
            issuer=args.token_issuer,
            audience=args.token_audience,
        )
        auth = RemoteAuthProvider(
            token_verifier=token_verifier,
            authorization_servers=auth_servers,
            base_url=args.remote_base_url,
        )

    middlewares: List[
        Union[
            UserTokenMiddleware,
            ErrorHandlingMiddleware,
            RateLimitingMiddleware,
            TimingMiddleware,
            LoggingMiddleware,
            JWTClaimsLoggingMiddleware,
            EunomiaMcpMiddleware,
        ]
    ] = [
        ErrorHandlingMiddleware(include_traceback=True, transform_errors=True),
        RateLimitingMiddleware(max_requests_per_second=10.0, burst_capacity=20),
        TimingMiddleware(),
        LoggingMiddleware(),
        JWTClaimsLoggingMiddleware(),
    ]
    if config["enable_delegation"] or args.auth_type == "jwt":
        middlewares.insert(0, UserTokenMiddleware(config=config))

    if args.eunomia_type in ["embedded", "remote"]:
        try:
            from eunomia_mcp import create_eunomia_middleware

            policy_file = args.eunomia_policy_file or "mcp_policies.json"
            eunomia_endpoint = (
                args.eunomia_remote_url if args.eunomia_type == "remote" else None
            )
            eunomia_mw = create_eunomia_middleware(
                policy_file=policy_file, eunomia_endpoint=eunomia_endpoint
            )
            middlewares.append(eunomia_mw)
            logger.info(f"Eunomia middleware enabled ({args.eunomia_type})")
        except Exception as e:
            print(f"Failed to load Eunomia middleware: {e}")
            logger.error("Failed to load Eunomia middleware", extra={"error": str(e)})
            sys.exit(1)

    mcp = FastMCP("Mealie", auth=auth)
    register_tools(mcp)
    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    print("\nStarting Mealie MCP Server")
    print(f"  Transport: {args.transport.upper()}")
    print(f"  Auth: {args.auth_type}")
    print(f"  Delegation: {'ON' if config['enable_delegation'] else 'OFF'}")
    print(f"  Eunomia: {args.eunomia_type}")

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mealie_mcp()
