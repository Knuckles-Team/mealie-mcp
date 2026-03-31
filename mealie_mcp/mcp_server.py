#!/usr/bin/python


from dotenv import load_dotenv, find_dotenv
import os
import sys
import logging
from typing import Optional, List, Dict, Any

from pydantic import Field
from fastmcp import FastMCP, Context
from fastmcp.utilities.logging import get_logger
from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import (
    create_mcp_server,
)
from mealie_mcp.api_wrapper import Api

__version__ = "0.2.51"
print(f"Mealie MCP v{__version__}", file=sys.stderr)

logger = get_logger(name="TokenMiddleware")
logger.setLevel(logging.DEBUG)


def register_prompts(mcp: FastMCP):
    @mcp.prompt(name="find_recipe", description="Find a recipe in your cookbook.")
    def find_recipe(query: str) -> str:
        """Find a recipe."""
        return f"Please find the recipe '{query}'"

    @mcp.prompt(name="random_meal", description="Suggest a random meal.")
    def random_meal() -> str:
        """Suggest a random meal."""
        return "Please suggest a random meal."


def register_misc_tools(mcp: FastMCP):
    async def health_check() -> Dict:
        return {"status": "OK"}


def register_app_tools(mcp: FastMCP):
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


def register_users_tools(mcp: FastMCP):
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


def register_households_tools(mcp: FastMCP):
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


def register_groups_tools(mcp: FastMCP):
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


def register_recipes_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["mealie_base_url", "mealie_token", "mealie_verify"],
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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
        tags={"recipes"},
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


def register_organizer_tools(mcp: FastMCP):
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


def register_shared_tools(mcp: FastMCP):
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


def register_admin_tools(mcp: FastMCP):
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


def register_explore_tools(mcp: FastMCP):
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


def register_utils_tools(mcp: FastMCP):
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


def get_mcp_instance() -> tuple[Any, Any, Any, Any]:
    """Initialize and return the MCP instance, args, and middlewares."""
    load_dotenv(find_dotenv())

    args, mcp, middlewares = create_mcp_server(
        name="Mealie",
        version=__version__,
        instructions="Mealie Recipe Manager MCP Server - Manage recipes, meal plans, shopping lists, and users.",
    )

    DEFAULT_MISCTOOL = to_boolean(os.getenv("MISCTOOL", "True"))
    if DEFAULT_MISCTOOL:
        register_misc_tools(mcp)
    DEFAULT_APPTOOL = to_boolean(os.getenv("APPTOOL", "True"))
    if DEFAULT_APPTOOL:
        register_app_tools(mcp)
    DEFAULT_USERSTOOL = to_boolean(os.getenv("USERSTOOL", "True"))
    if DEFAULT_USERSTOOL:
        register_users_tools(mcp)
    DEFAULT_HOUSEHOLDSTOOL = to_boolean(os.getenv("HOUSEHOLDSTOOL", "True"))
    if DEFAULT_HOUSEHOLDSTOOL:
        register_households_tools(mcp)
    DEFAULT_GROUPSTOOL = to_boolean(os.getenv("GROUPSTOOL", "True"))
    if DEFAULT_GROUPSTOOL:
        register_groups_tools(mcp)
    DEFAULT_RECIPESTOOL = to_boolean(os.getenv("RECIPESTOOL", "True"))
    if DEFAULT_RECIPESTOOL:
        register_recipes_tools(mcp)
    DEFAULT_ORGANIZERTOOL = to_boolean(os.getenv("ORGANIZERTOOL", "True"))
    if DEFAULT_ORGANIZERTOOL:
        register_organizer_tools(mcp)
    DEFAULT_SHAREDTOOL = to_boolean(os.getenv("SHAREDTOOL", "True"))
    if DEFAULT_SHAREDTOOL:
        register_shared_tools(mcp)
    DEFAULT_ADMINTOOL = to_boolean(os.getenv("ADMINTOOL", "True"))
    if DEFAULT_ADMINTOOL:
        register_admin_tools(mcp)
    DEFAULT_EXPLORETOOL = to_boolean(os.getenv("EXPLORETOOL", "True"))
    if DEFAULT_EXPLORETOOL:
        register_explore_tools(mcp)
    DEFAULT_UTILSTOOL = to_boolean(os.getenv("UTILSTOOL", "True"))
    if DEFAULT_UTILSTOOL:
        register_utils_tools(mcp)
    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)
    registered_tags = []
    return mcp, args, middlewares, registered_tags


def mcp_server() -> None:
    mcp, args, middlewares, registered_tags = get_mcp_instance()
    print(f"{args.name or 'mealie-mcp'} MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)
    print(f"  Dynamic Tags Loaded: {len(set(registered_tags))}", file=sys.stderr)

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
    mcp_server()
