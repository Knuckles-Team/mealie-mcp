#!/usr/bin/python
import warnings

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import os
import sys
from typing import Any

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_server
from dotenv import find_dotenv, load_dotenv
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse

from mealie_mcp.auth import get_client

__version__ = "0.12.0"

logger = get_logger(name="mealie-mcp")
logger.setLevel(logging.INFO)


def register_app_tools(mcp: FastMCP):
    @mcp.tool(tags={"app"})
    async def mealie_app(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_startup_info', 'get_app_theme'"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage app operations.

        Actions:
          - 'get_startup_info': Get Startup Info
          - 'get_app_theme': Get App Theme
        """
        kwargs: dict[str, Any]
        if action == "get_startup_info":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_startup_info(**kwargs)
        if action == "get_app_theme":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_app_theme(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_startup_info', 'get_app_theme"
        )


def register_users_tools(mcp: FastMCP):
    @mcp.tool(tags={"users"})
    async def mealie_users(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_token', 'oauth_login', 'oauth_callback', 'refresh_token', 'logout', 'register_new_user', 'get_logged_in_user', 'get_logged_in_user_ratings', 'get_logged_in_user_rating_for_recipe', 'get_logged_in_user_favorites', 'update_password', 'update_user', 'forgot_password', 'reset_password', 'update_user_image', 'create', 'delete', 'get_ratings', 'get_favorites', 'set_rating', 'add_favorite', 'remove_favorite'"
        ),
        data: Any | None = Field(default=None, description="data"),
        accept_language: Any | None = Field(
            default=None, description="accept language"
        ),
        recipe_id: str | None = Field(default=None, description="recipe id"),
        item_id: str | None = Field(default=None, description="item id"),
        id: str | None = Field(default=None, description="id"),
        token_id: int | None = Field(default=None, description="token id"),
        slug: str | None = Field(default=None, description="slug"),
        client=Depends(get_client),
    ) -> dict:
        """Manage users operations.

        Actions:
          - 'get_token': Get Token
          - 'oauth_login': Oauth Login
          - 'oauth_callback': Oauth Callback
          - 'refresh_token': Refresh Token
          - 'logout': Logout
          - 'register_new_user': Register New User
          - 'get_logged_in_user': Get Logged In User
          - 'get_logged_in_user_ratings': Get Logged In User Ratings
          - 'get_logged_in_user_rating_for_recipe': Get Logged In User Rating For Recipe
          - 'get_logged_in_user_favorites': Get Logged In User Favorites
          - 'update_password': Update Password
          - 'update_user': Update User
          - 'forgot_password': Forgot Password
          - 'reset_password': Reset Password
          - 'update_user_image': Update User Image
          - 'create': Create Api Token
          - 'delete': Delete Api Token
          - 'get_ratings': Get Ratings
          - 'get_favorites': Get Favorites
          - 'set_rating': Set Rating
          - 'add_favorite': Add Favorite
          - 'remove_favorite': Remove Favorite
        """
        kwargs: dict[str, Any]
        if action == "get_token":
            kwargs = {"data": data}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_token(**kwargs)
        if action == "oauth_login":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.oauth_login(**kwargs)
        if action == "oauth_callback":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.oauth_callback(**kwargs)
        if action == "refresh_token":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.refresh_token(**kwargs)
        if action == "logout":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.logout(**kwargs)
        if action == "register_new_user":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.register_new_user(**kwargs)
        if action == "get_logged_in_user":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_logged_in_user(**kwargs)
        if action == "get_logged_in_user_ratings":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_logged_in_user_ratings(**kwargs)
        if action == "get_logged_in_user_rating_for_recipe":
            kwargs = {
                "recipe_id": recipe_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_logged_in_user_rating_for_recipe(**kwargs)
        if action == "get_logged_in_user_favorites":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_logged_in_user_favorites(**kwargs)
        if action == "update_password":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_password(**kwargs)
        if action == "update_user":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_user(**kwargs)
        if action == "forgot_password":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.forgot_password(**kwargs)
        if action == "reset_password":
            kwargs = {"data": data}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.reset_password(**kwargs)
        if action == "update_user_image":
            kwargs = {
                "id": id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_user_image(**kwargs)
        if action == "create":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create(**kwargs)
        if action == "delete":
            kwargs = {
                "token_id": token_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete(**kwargs)
        if action == "get_ratings":
            kwargs = {"id": id, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_ratings(**kwargs)
        if action == "get_favorites":
            kwargs = {"id": id, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_favorites(**kwargs)
        if action == "set_rating":
            kwargs = {
                "id": id,
                "slug": slug,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_rating(**kwargs)
        if action == "add_favorite":
            kwargs = {
                "id": id,
                "slug": slug,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_favorite(**kwargs)
        if action == "remove_favorite":
            kwargs = {
                "id": id,
                "slug": slug,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.remove_favorite(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_token', 'oauth_login', 'oauth_callback', 'refresh_token', 'logout', 'register_new_user', 'get_logged_in_user', 'get_logged_in_user_ratings', 'get_logged_in_user_rating_for_recipe', 'get_logged_in_user_favorites', 'update_password', 'update_user', 'forgot_password', 'reset_password', 'update_user_image', 'create', 'delete', 'get_ratings', 'get_favorites', 'set_rating', 'add_favorite', 'remove_favorite"
        )


def register_households_tools(mcp: FastMCP):
    @mcp.tool(tags={"households"})
    async def mealie_households(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_households_cookbooks', 'post_households_cookbooks', 'put_households_cookbooks', 'get_households_cookbooks_item_id', 'put_households_cookbooks_item_id', 'delete_households_cookbooks_item_id', 'get_households_events_notifications', 'post_households_events_notifications', 'get_households_events_notifications_item_id', 'put_households_events_notifications_item_id', 'delete_households_events_notifications_item_id', 'test_notification', 'get_households_recipe_actions', 'post_households_recipe_actions', 'get_households_recipe_actions_item_id', 'put_households_recipe_actions_item_id', 'delete_households_recipe_actions_item_id', 'trigger_action', 'get_logged_in_user_household', 'get_household_recipe', 'get_household_members', 'get_household_preferences', 'update_household_preferences', 'set_member_permissions', 'get_statistics', 'get_invite_tokens', 'create_invite_token', 'email_invitation', 'get_households_shopping_lists', 'post_households_shopping_lists', 'get_households_shopping_lists_item_id', 'put_households_shopping_lists_item_id', 'delete_households_shopping_lists_item_id', 'update_label_settings', 'add_recipe_ingredients_to_list', 'add_single_recipe_ingredients_to_list', 'remove_recipe_ingredients_from_list', 'get_households_shopping_items', 'post_households_shopping_items', 'put_households_shopping_items', 'delete_households_shopping_items', 'post_households_shopping_items_create_bulk', 'get_households_shopping_items_item_id', 'put_households_shopping_items_item_id', 'delete_households_shopping_items_item_id', 'get_households_webhooks', 'post_households_webhooks', 'rerun_webhooks', 'get_households_webhooks_item_id', 'put_households_webhooks_item_id', 'delete_households_webhooks_item_id', 'test_one', 'get_households_mealplans_rules', 'post_households_mealplans_rules', 'get_households_mealplans_rules_item_id', 'put_households_mealplans_rules_item_id', 'delete_households_mealplans_rules_item_id', 'get_households_mealplans', 'post_households_mealplans', 'get_todays_meals', 'create_random_meal', 'get_households_mealplans_item_id', 'put_households_mealplans_item_id', 'delete_households_mealplans_item_id'"
        ),
        order_by: Any | None = Field(default=None, description="order by"),
        order_by_null_position: Any | None = Field(
            default=None, description="order by null position"
        ),
        order_direction: Any | None = Field(
            default=None, description="order direction"
        ),
        query_filter: Any | None = Field(default=None, description="query filter"),
        pagination_seed: Any | None = Field(
            default=None, description="pagination seed"
        ),
        page: int | None = Field(default=None, description="page"),
        per_page: int | None = Field(default=None, description="per page"),
        accept_language: Any | None = Field(
            default=None, description="accept language"
        ),
        data: Any | None = Field(default=None, description="data"),
        item_id: Any | None = Field(default=None, description="item id"),
        recipe_slug: str | None = Field(default=None, description="recipe slug"),
        recipe_id: str | None = Field(default=None, description="recipe id"),
        ids: list | None = Field(default=None, description="ids"),
        start_date: Any | None = Field(default=None, description="start date"),
        end_date: Any | None = Field(default=None, description="end date"),
        client=Depends(get_client),
    ) -> dict:
        """Manage households operations.

        Actions:
          - 'get_households_cookbooks': Get All
          - 'post_households_cookbooks': Create One
          - 'put_households_cookbooks': Update Many
          - 'get_households_cookbooks_item_id': Get One
          - 'put_households_cookbooks_item_id': Update One
          - 'delete_households_cookbooks_item_id': Delete One
          - 'get_households_events_notifications': Get All
          - 'post_households_events_notifications': Create One
          - 'get_households_events_notifications_item_id': Get One
          - 'put_households_events_notifications_item_id': Update One
          - 'delete_households_events_notifications_item_id': Delete One
          - 'test_notification': Test Notification
          - 'get_households_recipe_actions': Get All
          - 'post_households_recipe_actions': Create One
          - 'get_households_recipe_actions_item_id': Get One
          - 'put_households_recipe_actions_item_id': Update One
          - 'delete_households_recipe_actions_item_id': Delete One
          - 'trigger_action': Trigger Action
          - 'get_logged_in_user_household': Get Logged In User Household
          - 'get_household_recipe': Get Household Recipe
          - 'get_household_members': Get Household Members
          - 'get_household_preferences': Get Household Preferences
          - 'update_household_preferences': Update Household Preferences
          - 'set_member_permissions': Set Member Permissions
          - 'get_statistics': Get Statistics
          - 'get_invite_tokens': Get Invite Tokens
          - 'create_invite_token': Create Invite Token
          - 'email_invitation': Email Invitation
          - 'get_households_shopping_lists': Get All
          - 'post_households_shopping_lists': Create One
          - 'get_households_shopping_lists_item_id': Get One
          - 'put_households_shopping_lists_item_id': Update One
          - 'delete_households_shopping_lists_item_id': Delete One
          - 'update_label_settings': Update Label Settings
          - 'add_recipe_ingredients_to_list': Add Recipe Ingredients To List
          - 'add_single_recipe_ingredients_to_list': Add Single Recipe Ingredients To List
          - 'remove_recipe_ingredients_from_list': Remove Recipe Ingredients From List
          - 'get_households_shopping_items': Get All
          - 'post_households_shopping_items': Create One
          - 'put_households_shopping_items': Update Many
          - 'delete_households_shopping_items': Delete Many
          - 'post_households_shopping_items_create_bulk': Create Many
          - 'get_households_shopping_items_item_id': Get One
          - 'put_households_shopping_items_item_id': Update One
          - 'delete_households_shopping_items_item_id': Delete One
          - 'get_households_webhooks': Get All
          - 'post_households_webhooks': Create One
          - 'rerun_webhooks': Rerun Webhooks
          - 'get_households_webhooks_item_id': Get One
          - 'put_households_webhooks_item_id': Update One
          - 'delete_households_webhooks_item_id': Delete One
          - 'test_one': Test One
          - 'get_households_mealplans_rules': Get All
          - 'post_households_mealplans_rules': Create One
          - 'get_households_mealplans_rules_item_id': Get One
          - 'put_households_mealplans_rules_item_id': Update One
          - 'delete_households_mealplans_rules_item_id': Delete One
          - 'get_households_mealplans': Get All
          - 'post_households_mealplans': Create One
          - 'get_todays_meals': Get Todays Meals
          - 'create_random_meal': Create Random Meal
          - 'get_households_mealplans_item_id': Get One
          - 'put_households_mealplans_item_id': Update One
          - 'delete_households_mealplans_item_id': Delete One
        """
        kwargs: dict[str, Any]
        if action == "get_households_cookbooks":
            kwargs = {
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_households_cookbooks(**kwargs)
        if action == "post_households_cookbooks":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_households_cookbooks(**kwargs)
        if action == "put_households_cookbooks":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_households_cookbooks(**kwargs)
        if action == "get_households_cookbooks_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_households_cookbooks_item_id(**kwargs)
        if action == "put_households_cookbooks_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_households_cookbooks_item_id(**kwargs)
        if action == "delete_households_cookbooks_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_households_cookbooks_item_id(**kwargs)
        if action == "get_households_events_notifications":
            kwargs = {
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_households_events_notifications(**kwargs)
        if action == "post_households_events_notifications":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_households_events_notifications(**kwargs)
        if action == "get_households_events_notifications_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_households_events_notifications_item_id(**kwargs)
        if action == "put_households_events_notifications_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_households_events_notifications_item_id(**kwargs)
        if action == "delete_households_events_notifications_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_households_events_notifications_item_id(**kwargs)
        if action == "test_notification":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.test_notification(**kwargs)
        if action == "get_households_recipe_actions":
            kwargs = {
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_households_recipe_actions(**kwargs)
        if action == "post_households_recipe_actions":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_households_recipe_actions(**kwargs)
        if action == "get_households_recipe_actions_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_households_recipe_actions_item_id(**kwargs)
        if action == "put_households_recipe_actions_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_households_recipe_actions_item_id(**kwargs)
        if action == "delete_households_recipe_actions_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_households_recipe_actions_item_id(**kwargs)
        if action == "trigger_action":
            kwargs = {
                "item_id": item_id,
                "recipe_slug": recipe_slug,
                "accept_language": accept_language,
                "data": data,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.trigger_action(**kwargs)
        if action == "get_logged_in_user_household":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_logged_in_user_household(**kwargs)
        if action == "get_household_recipe":
            kwargs = {
                "recipe_slug": recipe_slug,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_household_recipe(**kwargs)
        if action == "get_household_members":
            kwargs = {
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_household_members(**kwargs)
        if action == "get_household_preferences":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_household_preferences(**kwargs)
        if action == "update_household_preferences":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_household_preferences(**kwargs)
        if action == "set_member_permissions":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.set_member_permissions(**kwargs)
        if action == "get_statistics":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_statistics(**kwargs)
        if action == "get_invite_tokens":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_invite_tokens(**kwargs)
        if action == "create_invite_token":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_invite_token(**kwargs)
        if action == "email_invitation":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.email_invitation(**kwargs)
        if action == "get_households_shopping_lists":
            kwargs = {
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_households_shopping_lists(**kwargs)
        if action == "post_households_shopping_lists":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_households_shopping_lists(**kwargs)
        if action == "get_households_shopping_lists_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_households_shopping_lists_item_id(**kwargs)
        if action == "put_households_shopping_lists_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_households_shopping_lists_item_id(**kwargs)
        if action == "delete_households_shopping_lists_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_households_shopping_lists_item_id(**kwargs)
        if action == "update_label_settings":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_label_settings(**kwargs)
        if action == "add_recipe_ingredients_to_list":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_recipe_ingredients_to_list(**kwargs)
        if action == "add_single_recipe_ingredients_to_list":
            kwargs = {
                "item_id": item_id,
                "recipe_id": recipe_id,
                "accept_language": accept_language,
                "data": data,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_single_recipe_ingredients_to_list(**kwargs)
        if action == "remove_recipe_ingredients_from_list":
            kwargs = {
                "item_id": item_id,
                "recipe_id": recipe_id,
                "accept_language": accept_language,
                "data": data,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.remove_recipe_ingredients_from_list(**kwargs)
        if action == "get_households_shopping_items":
            kwargs = {
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_households_shopping_items(**kwargs)
        if action == "post_households_shopping_items":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_households_shopping_items(**kwargs)
        if action == "put_households_shopping_items":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_households_shopping_items(**kwargs)
        if action == "delete_households_shopping_items":
            kwargs = {"ids": ids, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_households_shopping_items(**kwargs)
        if action == "post_households_shopping_items_create_bulk":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_households_shopping_items_create_bulk(**kwargs)
        if action == "get_households_shopping_items_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_households_shopping_items_item_id(**kwargs)
        if action == "put_households_shopping_items_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_households_shopping_items_item_id(**kwargs)
        if action == "delete_households_shopping_items_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_households_shopping_items_item_id(**kwargs)
        if action == "get_households_webhooks":
            kwargs = {
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_households_webhooks(**kwargs)
        if action == "post_households_webhooks":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_households_webhooks(**kwargs)
        if action == "rerun_webhooks":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.rerun_webhooks(**kwargs)
        if action == "get_households_webhooks_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_households_webhooks_item_id(**kwargs)
        if action == "put_households_webhooks_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_households_webhooks_item_id(**kwargs)
        if action == "delete_households_webhooks_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_households_webhooks_item_id(**kwargs)
        if action == "test_one":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.test_one(**kwargs)
        if action == "get_households_mealplans_rules":
            kwargs = {
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_households_mealplans_rules(**kwargs)
        if action == "post_households_mealplans_rules":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_households_mealplans_rules(**kwargs)
        if action == "get_households_mealplans_rules_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_households_mealplans_rules_item_id(**kwargs)
        if action == "put_households_mealplans_rules_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_households_mealplans_rules_item_id(**kwargs)
        if action == "delete_households_mealplans_rules_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_households_mealplans_rules_item_id(**kwargs)
        if action == "get_households_mealplans":
            kwargs = {
                "start_date": start_date,
                "end_date": end_date,
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_households_mealplans(**kwargs)
        if action == "post_households_mealplans":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_households_mealplans(**kwargs)
        if action == "get_todays_meals":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_todays_meals(**kwargs)
        if action == "create_random_meal":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_random_meal(**kwargs)
        if action == "get_households_mealplans_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_households_mealplans_item_id(**kwargs)
        if action == "put_households_mealplans_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_households_mealplans_item_id(**kwargs)
        if action == "delete_households_mealplans_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_households_mealplans_item_id(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_households_cookbooks', 'post_households_cookbooks', 'put_households_cookbooks', 'get_households_cookbooks_item_id', 'put_households_cookbooks_item_id', 'delete_households_cookbooks_item_id', 'get_households_events_notifications', 'post_households_events_notifications', 'get_households_events_notifications_item_id', 'put_households_events_notifications_item_id', 'delete_households_events_notifications_item_id', 'test_notification', 'get_households_recipe_actions', 'post_households_recipe_actions', 'get_households_recipe_actions_item_id', 'put_households_recipe_actions_item_id', 'delete_households_recipe_actions_item_id', 'trigger_action', 'get_logged_in_user_household', 'get_household_recipe', 'get_household_members', 'get_household_preferences', 'update_household_preferences', 'set_member_permissions', 'get_statistics', 'get_invite_tokens', 'create_invite_token', 'email_invitation', 'get_households_shopping_lists', 'post_households_shopping_lists', 'get_households_shopping_lists_item_id', 'put_households_shopping_lists_item_id', 'delete_households_shopping_lists_item_id', 'update_label_settings', 'add_recipe_ingredients_to_list', 'add_single_recipe_ingredients_to_list', 'remove_recipe_ingredients_from_list', 'get_households_shopping_items', 'post_households_shopping_items', 'put_households_shopping_items', 'delete_households_shopping_items', 'post_households_shopping_items_create_bulk', 'get_households_shopping_items_item_id', 'put_households_shopping_items_item_id', 'delete_households_shopping_items_item_id', 'get_households_webhooks', 'post_households_webhooks', 'rerun_webhooks', 'get_households_webhooks_item_id', 'put_households_webhooks_item_id', 'delete_households_webhooks_item_id', 'test_one', 'get_households_mealplans_rules', 'post_households_mealplans_rules', 'get_households_mealplans_rules_item_id', 'put_households_mealplans_rules_item_id', 'delete_households_mealplans_rules_item_id', 'get_households_mealplans', 'post_households_mealplans', 'get_todays_meals', 'create_random_meal', 'get_households_mealplans_item_id', 'put_households_mealplans_item_id', 'delete_households_mealplans_item_id"
        )


def register_groups_tools(mcp: FastMCP):
    @mcp.tool(tags={"groups"})
    async def mealie_groups(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_all_households', 'get_one_household', 'get_logged_in_user_group', 'get_group_members', 'get_group_member', 'get_group_preferences', 'update_group_preferences', 'get_storage', 'start_data_migration', 'get_groups_reports', 'get_groups_reports_item_id', 'delete_groups_reports_item_id', 'get_groups_labels', 'post_groups_labels', 'get_groups_labels_item_id', 'put_groups_labels_item_id', 'delete_groups_labels_item_id', 'seed_foods', 'seed_labels', 'seed_units'"
        ),
        order_by: Any | None = Field(default=None, description="order by"),
        order_by_null_position: Any | None = Field(
            default=None, description="order by null position"
        ),
        order_direction: Any | None = Field(
            default=None, description="order direction"
        ),
        query_filter: Any | None = Field(default=None, description="query filter"),
        pagination_seed: Any | None = Field(
            default=None, description="pagination seed"
        ),
        page: int | None = Field(default=None, description="page"),
        per_page: int | None = Field(default=None, description="per page"),
        accept_language: Any | None = Field(
            default=None, description="accept language"
        ),
        household_slug: str | None = Field(default=None, description="household slug"),
        username_or_id: Any | None = Field(default=None, description="username or id"),
        data: dict | None = Field(default=None, description="data"),
        report_type: Any | None = Field(default=None, description="report type"),
        item_id: str | None = Field(default=None, description="item id"),
        search: Any | None = Field(default=None, description="search"),
        client=Depends(get_client),
    ) -> dict:
        """Manage groups operations.

        Actions:
          - 'get_all_households': Get All Households
          - 'get_one_household': Get One Household
          - 'get_logged_in_user_group': Get Logged In User Group
          - 'get_group_members': Get Group Members
          - 'get_group_member': Get Group Member
          - 'get_group_preferences': Get Group Preferences
          - 'update_group_preferences': Update Group Preferences
          - 'get_storage': Get Storage
          - 'start_data_migration': Start Data Migration
          - 'get_groups_reports': Get All
          - 'get_groups_reports_item_id': Get One
          - 'delete_groups_reports_item_id': Delete One
          - 'get_groups_labels': Get All
          - 'post_groups_labels': Create One
          - 'get_groups_labels_item_id': Get One
          - 'put_groups_labels_item_id': Update One
          - 'delete_groups_labels_item_id': Delete One
          - 'seed_foods': Seed Foods
          - 'seed_labels': Seed Labels
          - 'seed_units': Seed Units
        """
        kwargs: dict[str, Any]
        if action == "get_all_households":
            kwargs = {
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_all_households(**kwargs)
        if action == "get_one_household":
            kwargs = {
                "household_slug": household_slug,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_one_household(**kwargs)
        if action == "get_logged_in_user_group":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_logged_in_user_group(**kwargs)
        if action == "get_group_members":
            kwargs = {
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_group_members(**kwargs)
        if action == "get_group_member":
            kwargs = {
                "username_or_id": username_or_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_group_member(**kwargs)
        if action == "get_group_preferences":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_group_preferences(**kwargs)
        if action == "update_group_preferences":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_group_preferences(**kwargs)
        if action == "get_storage":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_storage(**kwargs)
        if action == "start_data_migration":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.start_data_migration(**kwargs)
        if action == "get_groups_reports":
            kwargs = {
                "report_type": report_type,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_groups_reports(**kwargs)
        if action == "get_groups_reports_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_groups_reports_item_id(**kwargs)
        if action == "delete_groups_reports_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_groups_reports_item_id(**kwargs)
        if action == "get_groups_labels":
            kwargs = {
                "search": search,
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_groups_labels(**kwargs)
        if action == "post_groups_labels":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_groups_labels(**kwargs)
        if action == "get_groups_labels_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_groups_labels_item_id(**kwargs)
        if action == "put_groups_labels_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_groups_labels_item_id(**kwargs)
        if action == "delete_groups_labels_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_groups_labels_item_id(**kwargs)
        if action == "seed_foods":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.seed_foods(**kwargs)
        if action == "seed_labels":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.seed_labels(**kwargs)
        if action == "seed_units":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.seed_units(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_all_households', 'get_one_household', 'get_logged_in_user_group', 'get_group_members', 'get_group_member', 'get_group_preferences', 'update_group_preferences', 'get_storage', 'start_data_migration', 'get_groups_reports', 'get_groups_reports_item_id', 'delete_groups_reports_item_id', 'get_groups_labels', 'post_groups_labels', 'get_groups_labels_item_id', 'put_groups_labels_item_id', 'delete_groups_labels_item_id', 'seed_foods', 'seed_labels', 'seed_units"
        )


def register_recipes_tools(mcp: FastMCP):
    @mcp.tool(tags={"recipes"})
    async def mealie_recipes(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_recipe_formats_and_templates', 'get_recipe_as_format', 'test_parse_recipe_url', 'create_recipe_from_html_or_json', 'parse_recipe_url', 'parse_recipe_url_bulk', 'create_recipe_from_zip', 'create_recipe_from_image', 'get_recipes', 'post_recipes', 'put_recipes', 'patch_many', 'get_recipes_suggestions', 'get_recipes_slug', 'put_recipes_slug', 'patch_one', 'delete_recipes_slug', 'duplicate_one', 'update_last_made', 'scrape_image_url', 'update_recipe_image', 'delete_recipe_image', 'upload_recipe_asset', 'get_recipe_comments', 'bulk_tag_recipes', 'bulk_settings_recipes', 'bulk_categorize_recipes', 'bulk_delete_recipes', 'bulk_export_recipes', 'get_exported_data', 'get_exported_data_token', 'purge_export_data', 'get_shared_recipe', 'get_shared_recipe_as_zip', 'get_recipes_timeline_events', 'post_recipes_timeline_events', 'get_recipes_timeline_events_item_id', 'put_recipes_timeline_events_item_id', 'delete_recipes_timeline_events_item_id', 'update_event_image', 'get_comments', 'post_comments', 'get_comments_item_id', 'put_comments_item_id', 'post_parser_ingredient', 'parse_ingredient', 'parse_ingredients', 'get_foods', 'post_foods', 'put_foods_merge', 'get_foods_item_id', 'put_foods_item_id', 'delete_foods_item_id', 'get_units', 'post_units', 'put_units_merge', 'get_units_item_id', 'put_units_item_id', 'delete_units_item_id', 'get_recipe_img', 'get_recipe_timeline_event_img', 'get_recipe_asset', 'get_user_image', 'get_validation_text'"
        ),
        accept_language: Any | None = Field(
            default=None, description="accept language"
        ),
        slug: str | None = Field(default=None, description="slug"),
        template_name: str | None = Field(default=None, description="template name"),
        data: dict | None = Field(default=None, description="data"),
        translate_language: Any | None = Field(
            default=None, description="translate language"
        ),
        categories: Any | None = Field(default=None, description="categories"),
        tags: Any | None = Field(default=None, description="tags"),
        tools: Any | None = Field(default=None, description="tools"),
        foods: Any | None = Field(default=None, description="foods"),
        households: Any | None = Field(default=None, description="households"),
        order_by: Any | None = Field(default=None, description="order by"),
        order_by_null_position: Any | None = Field(
            default=None, description="order by null position"
        ),
        order_direction: Any | None = Field(
            default=None, description="order direction"
        ),
        query_filter: Any | None = Field(default=None, description="query filter"),
        pagination_seed: Any | None = Field(
            default=None, description="pagination seed"
        ),
        page: int | None = Field(default=None, description="page"),
        per_page: int | None = Field(default=None, description="per page"),
        cookbook: Any | None = Field(default=None, description="cookbook"),
        require_all_categories: bool | None = Field(
            default=None, description="require all categories"
        ),
        require_all_tags: bool | None = Field(
            default=None, description="require all tags"
        ),
        require_all_tools: bool | None = Field(
            default=None, description="require all tools"
        ),
        require_all_foods: bool | None = Field(
            default=None, description="require all foods"
        ),
        search: Any | None = Field(default=None, description="search"),
        limit: int | None = Field(default=None, description="limit"),
        max_missing_foods: int | None = Field(
            default=None, description="max missing foods"
        ),
        max_missing_tools: int | None = Field(
            default=None, description="max missing tools"
        ),
        include_foods_on_hand: bool | None = Field(
            default=None, description="include foods on hand"
        ),
        include_tools_on_hand: bool | None = Field(
            default=None, description="include tools on hand"
        ),
        export_id: str | None = Field(default=None, description="export id"),
        token_id: str | None = Field(default=None, description="token id"),
        item_id: str | None = Field(default=None, description="item id"),
        recipe_id: str | None = Field(default=None, description="recipe id"),
        file_name: Any | None = Field(default=None, description="file name"),
        timeline_event_id: str | None = Field(
            default=None, description="timeline event id"
        ),
        user_id: str | None = Field(default=None, description="user id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage recipes operations.

        Actions:
          - 'get_recipe_formats_and_templates': Get Recipe Formats And Templates
          - 'get_recipe_as_format': Get Recipe As Format
          - 'test_parse_recipe_url': Test Parse Recipe Url
          - 'create_recipe_from_html_or_json': Create Recipe From Html Or Json
          - 'parse_recipe_url': Parse Recipe Url
          - 'parse_recipe_url_bulk': Parse Recipe Url Bulk
          - 'create_recipe_from_zip': Create Recipe From Zip
          - 'create_recipe_from_image': Create Recipe From Image
          - 'get_recipes': Get All
          - 'post_recipes': Create One
          - 'put_recipes': Update Many
          - 'patch_many': Patch Many
          - 'get_recipes_suggestions': Suggest Recipes
          - 'get_recipes_slug': Get One
          - 'put_recipes_slug': Update One
          - 'patch_one': Patch One
          - 'delete_recipes_slug': Delete One
          - 'duplicate_one': Duplicate One
          - 'update_last_made': Update Last Made
          - 'scrape_image_url': Scrape Image Url
          - 'update_recipe_image': Update Recipe Image
          - 'delete_recipe_image': Delete Recipe Image
          - 'upload_recipe_asset': Upload Recipe Asset
          - 'get_recipe_comments': Get Recipe Comments
          - 'bulk_tag_recipes': Bulk Tag Recipes
          - 'bulk_settings_recipes': Bulk Settings Recipes
          - 'bulk_categorize_recipes': Bulk Categorize Recipes
          - 'bulk_delete_recipes': Bulk Delete Recipes
          - 'bulk_export_recipes': Bulk Export Recipes
          - 'get_exported_data': Get Exported Data
          - 'get_exported_data_token': Get Exported Data Token
          - 'purge_export_data': Purge Export Data
          - 'get_shared_recipe': Get Shared Recipe
          - 'get_shared_recipe_as_zip': Get Shared Recipe As Zip
          - 'get_recipes_timeline_events': Get All
          - 'post_recipes_timeline_events': Create One
          - 'get_recipes_timeline_events_item_id': Get One
          - 'put_recipes_timeline_events_item_id': Update One
          - 'delete_recipes_timeline_events_item_id': Delete One
          - 'update_event_image': Update Event Image
          - 'get_comments': Get All
          - 'post_comments': Create One
          - 'get_comments_item_id': Get One
          - 'put_comments_item_id': Update One
          - 'post_parser_ingredient': Delete One
          - 'parse_ingredient': Parse Ingredient
          - 'parse_ingredients': Parse Ingredients
          - 'get_foods': Get All
          - 'post_foods': Create One
          - 'put_foods_merge': Merge One
          - 'get_foods_item_id': Get One
          - 'put_foods_item_id': Update One
          - 'delete_foods_item_id': Delete One
          - 'get_units': Get All
          - 'post_units': Create One
          - 'put_units_merge': Merge One
          - 'get_units_item_id': Get One
          - 'put_units_item_id': Update One
          - 'delete_units_item_id': Delete One
          - 'get_recipe_img': Get Recipe Img
          - 'get_recipe_timeline_event_img': Get Recipe Timeline Event Img
          - 'get_recipe_asset': Get Recipe Asset
          - 'get_user_image': Get User Image
          - 'get_validation_text': Get Validation Text
        """
        kwargs: dict[str, Any]
        if action == "get_recipe_formats_and_templates":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recipe_formats_and_templates(**kwargs)
        if action == "get_recipe_as_format":
            kwargs = {
                "slug": slug,
                "template_name": template_name,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recipe_as_format(**kwargs)
        if action == "test_parse_recipe_url":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.test_parse_recipe_url(**kwargs)
        if action == "create_recipe_from_html_or_json":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_recipe_from_html_or_json(**kwargs)
        if action == "parse_recipe_url":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.parse_recipe_url(**kwargs)
        if action == "parse_recipe_url_bulk":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.parse_recipe_url_bulk(**kwargs)
        if action == "create_recipe_from_zip":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_recipe_from_zip(**kwargs)
        if action == "create_recipe_from_image":
            kwargs = {
                "data": data,
                "translate_language": translate_language,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_recipe_from_image(**kwargs)
        if action == "get_recipes":
            kwargs = {
                "categories": categories,
                "tags": tags,
                "tools": tools,
                "foods": foods,
                "households": households,
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "cookbook": cookbook,
                "require_all_categories": require_all_categories,
                "require_all_tags": require_all_tags,
                "require_all_tools": require_all_tools,
                "require_all_foods": require_all_foods,
                "search": search,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recipes(**kwargs)
        if action == "post_recipes":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_recipes(**kwargs)
        if action == "put_recipes":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_recipes(**kwargs)
        if action == "patch_many":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.patch_many(**kwargs)
        if action == "get_recipes_suggestions":
            kwargs = {
                "foods": foods,
                "tools": tools,
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "limit": limit,
                "max_missing_foods": max_missing_foods,
                "max_missing_tools": max_missing_tools,
                "include_foods_on_hand": include_foods_on_hand,
                "include_tools_on_hand": include_tools_on_hand,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recipes_suggestions(**kwargs)
        if action == "get_recipes_slug":
            kwargs = {"slug": slug, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recipes_slug(**kwargs)
        if action == "put_recipes_slug":
            kwargs = {
                "slug": slug,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_recipes_slug(**kwargs)
        if action == "patch_one":
            kwargs = {
                "slug": slug,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.patch_one(**kwargs)
        if action == "delete_recipes_slug":
            kwargs = {"slug": slug, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_recipes_slug(**kwargs)
        if action == "duplicate_one":
            kwargs = {
                "slug": slug,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.duplicate_one(**kwargs)
        if action == "update_last_made":
            kwargs = {
                "slug": slug,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_last_made(**kwargs)
        if action == "scrape_image_url":
            kwargs = {
                "slug": slug,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.scrape_image_url(**kwargs)
        if action == "update_recipe_image":
            kwargs = {
                "slug": slug,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_recipe_image(**kwargs)
        if action == "delete_recipe_image":
            kwargs = {"slug": slug, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_recipe_image(**kwargs)
        if action == "upload_recipe_asset":
            kwargs = {
                "slug": slug,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.upload_recipe_asset(**kwargs)
        if action == "get_recipe_comments":
            kwargs = {"slug": slug, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recipe_comments(**kwargs)
        if action == "bulk_tag_recipes":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.bulk_tag_recipes(**kwargs)
        if action == "bulk_settings_recipes":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.bulk_settings_recipes(**kwargs)
        if action == "bulk_categorize_recipes":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.bulk_categorize_recipes(**kwargs)
        if action == "bulk_delete_recipes":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.bulk_delete_recipes(**kwargs)
        if action == "bulk_export_recipes":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.bulk_export_recipes(**kwargs)
        if action == "get_exported_data":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_exported_data(**kwargs)
        if action == "get_exported_data_token":
            kwargs = {
                "export_id": export_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_exported_data_token(**kwargs)
        if action == "purge_export_data":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.purge_export_data(**kwargs)
        if action == "get_shared_recipe":
            kwargs = {"token_id": token_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_shared_recipe(**kwargs)
        if action == "get_shared_recipe_as_zip":
            kwargs = {"token_id": token_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_shared_recipe_as_zip(**kwargs)
        if action == "get_recipes_timeline_events":
            kwargs = {
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recipes_timeline_events(**kwargs)
        if action == "post_recipes_timeline_events":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_recipes_timeline_events(**kwargs)
        if action == "get_recipes_timeline_events_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recipes_timeline_events_item_id(**kwargs)
        if action == "put_recipes_timeline_events_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_recipes_timeline_events_item_id(**kwargs)
        if action == "delete_recipes_timeline_events_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_recipes_timeline_events_item_id(**kwargs)
        if action == "update_event_image":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_event_image(**kwargs)
        if action == "get_comments":
            kwargs = {
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_comments(**kwargs)
        if action == "post_comments":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_comments(**kwargs)
        if action == "get_comments_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_comments_item_id(**kwargs)
        if action == "put_comments_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_comments_item_id(**kwargs)
        if action == "post_parser_ingredient":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_parser_ingredient(**kwargs)
        if action == "parse_ingredient":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.parse_ingredient(**kwargs)
        if action == "parse_ingredients":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.parse_ingredients(**kwargs)
        if action == "get_foods":
            kwargs = {
                "search": search,
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_foods(**kwargs)
        if action == "post_foods":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_foods(**kwargs)
        if action == "put_foods_merge":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_foods_merge(**kwargs)
        if action == "get_foods_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_foods_item_id(**kwargs)
        if action == "put_foods_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_foods_item_id(**kwargs)
        if action == "delete_foods_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_foods_item_id(**kwargs)
        if action == "get_units":
            kwargs = {
                "search": search,
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_units(**kwargs)
        if action == "post_units":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_units(**kwargs)
        if action == "put_units_merge":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_units_merge(**kwargs)
        if action == "get_units_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_units_item_id(**kwargs)
        if action == "put_units_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_units_item_id(**kwargs)
        if action == "delete_units_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_units_item_id(**kwargs)
        if action == "get_recipe_img":
            kwargs = {"recipe_id": recipe_id, "file_name": file_name}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recipe_img(**kwargs)
        if action == "get_recipe_timeline_event_img":
            kwargs = {
                "recipe_id": recipe_id,
                "timeline_event_id": timeline_event_id,
                "file_name": file_name,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recipe_timeline_event_img(**kwargs)
        if action == "get_recipe_asset":
            kwargs = {"recipe_id": recipe_id, "file_name": file_name}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recipe_asset(**kwargs)
        if action == "get_user_image":
            kwargs = {"user_id": user_id, "file_name": file_name}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_user_image(**kwargs)
        if action == "get_validation_text":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_validation_text(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_recipe_formats_and_templates', 'get_recipe_as_format', 'test_parse_recipe_url', 'create_recipe_from_html_or_json', 'parse_recipe_url', 'parse_recipe_url_bulk', 'create_recipe_from_zip', 'create_recipe_from_image', 'get_recipes', 'post_recipes', 'put_recipes', 'patch_many', 'get_recipes_suggestions', 'get_recipes_slug', 'put_recipes_slug', 'patch_one', 'delete_recipes_slug', 'duplicate_one', 'update_last_made', 'scrape_image_url', 'update_recipe_image', 'delete_recipe_image', 'upload_recipe_asset', 'get_recipe_comments', 'bulk_tag_recipes', 'bulk_settings_recipes', 'bulk_categorize_recipes', 'bulk_delete_recipes', 'bulk_export_recipes', 'get_exported_data', 'get_exported_data_token', 'purge_export_data', 'get_shared_recipe', 'get_shared_recipe_as_zip', 'get_recipes_timeline_events', 'post_recipes_timeline_events', 'get_recipes_timeline_events_item_id', 'put_recipes_timeline_events_item_id', 'delete_recipes_timeline_events_item_id', 'update_event_image', 'get_comments', 'post_comments', 'get_comments_item_id', 'put_comments_item_id', 'post_parser_ingredient', 'parse_ingredient', 'parse_ingredients', 'get_foods', 'post_foods', 'put_foods_merge', 'get_foods_item_id', 'put_foods_item_id', 'delete_foods_item_id', 'get_units', 'post_units', 'put_units_merge', 'get_units_item_id', 'put_units_item_id', 'delete_units_item_id', 'get_recipe_img', 'get_recipe_timeline_event_img', 'get_recipe_asset', 'get_user_image', 'get_validation_text"
        )


def register_organizer_tools(mcp: FastMCP):
    @mcp.tool(tags={"organizer"})
    async def mealie_organizer(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_organizers_categories', 'post_organizers_categories', 'get_all_empty', 'get_organizers_categories_item_id', 'put_organizers_categories_item_id', 'delete_organizers_categories_item_id', 'get_organizers_categories_slug_category_slug', 'get_organizers_tags', 'post_organizers_tags', 'get_empty_tags', 'get_organizers_tags_item_id', 'put_organizers_tags_item_id', 'delete_recipe_tag', 'get_organizers_tags_slug_tag_slug', 'get_organizerss', 'post_organizerss', 'get_organizerss_item_id', 'put_organizerss_item_id', 'delete_organizerss_item_id', 'get_organizerss_slug_slug'"
        ),
        search: Any | None = Field(default=None, description="search"),
        order_by: Any | None = Field(default=None, description="order by"),
        order_by_null_position: Any | None = Field(
            default=None, description="order by null position"
        ),
        order_direction: Any | None = Field(
            default=None, description="order direction"
        ),
        query_filter: Any | None = Field(default=None, description="query filter"),
        pagination_seed: Any | None = Field(
            default=None, description="pagination seed"
        ),
        page: int | None = Field(default=None, description="page"),
        per_page: int | None = Field(default=None, description="per page"),
        accept_language: Any | None = Field(
            default=None, description="accept language"
        ),
        data: dict | None = Field(default=None, description="data"),
        item_id: str | None = Field(default=None, description="item id"),
        category_slug: str | None = Field(default=None, description="category slug"),
        tag_slug: str | None = Field(default=None, description="tag slug"),
        client=Depends(get_client),
    ) -> dict:
        """Manage organizer operations.

        Actions:
          - 'get_organizers_categories': Get All
          - 'post_organizers_categories': Create One
          - 'get_all_empty': Get All Empty
          - 'get_organizers_categories_item_id': Get One
          - 'put_organizers_categories_item_id': Update One
          - 'delete_organizers_categories_item_id': Delete One
          - 'get_organizers_categories_slug_category_slug': Get One By Slug
          - 'get_organizers_tags': Get All
          - 'post_organizers_tags': Create One
          - 'get_empty_tags': Get Empty Tags
          - 'get_organizers_tags_item_id': Get One
          - 'put_organizers_tags_item_id': Update One
          - 'delete_recipe_tag': Delete Recipe Tag
          - 'get_organizers_tags_slug_tag_slug': Get One By Slug
          - 'get_organizerss': Call get_organizerss
          - 'post_organizerss': Call post_organizerss
          - 'get_organizerss_item_id': Call get_organizerss_item_id
          - 'put_organizerss_item_id': Call put_organizerss_item_id
          - 'delete_organizerss_item_id': Call delete_organizerss_item_id
          - 'get_organizerss_slug_slug': Call get_organizerss_slug_slug
        """
        kwargs: dict[str, Any]
        if action == "get_organizers_categories":
            kwargs = {
                "search": search,
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_organizers_categories(**kwargs)
        if action == "post_organizers_categories":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_organizers_categories(**kwargs)
        if action == "get_all_empty":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_all_empty(**kwargs)
        if action == "get_organizers_categories_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_organizers_categories_item_id(**kwargs)
        if action == "put_organizers_categories_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_organizers_categories_item_id(**kwargs)
        if action == "delete_organizers_categories_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_organizers_categories_item_id(**kwargs)
        if action == "get_organizers_categories_slug_category_slug":
            kwargs = {
                "category_slug": category_slug,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_organizers_categories_slug_category_slug(**kwargs)
        if action == "get_organizers_tags":
            kwargs = {
                "search": search,
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_organizers_tags(**kwargs)
        if action == "post_organizers_tags":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_organizers_tags(**kwargs)
        if action == "get_empty_tags":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_empty_tags(**kwargs)
        if action == "get_organizers_tags_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_organizers_tags_item_id(**kwargs)
        if action == "put_organizers_tags_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_organizers_tags_item_id(**kwargs)
        if action == "delete_recipe_tag":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_recipe_tag(**kwargs)
        if action == "get_organizers_tags_slug_tag_slug":
            kwargs = {
                "tag_slug": tag_slug,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_organizers_tags_slug_tag_slug(**kwargs)
        if action == "get_organizerss":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_organizerss(**kwargs)
        if action == "post_organizerss":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_organizerss(**kwargs)
        if action == "get_organizerss_item_id":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_organizerss_item_id(**kwargs)
        if action == "put_organizerss_item_id":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_organizerss_item_id(**kwargs)
        if action == "delete_organizerss_item_id":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_organizerss_item_id(**kwargs)
        if action == "get_organizerss_slug_slug":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_organizerss_slug_slug(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_organizers_categories', 'post_organizers_categories', 'get_all_empty', 'get_organizers_categories_item_id', 'put_organizers_categories_item_id', 'delete_organizers_categories_item_id', 'get_organizers_categories_slug_category_slug', 'get_organizers_tags', 'post_organizers_tags', 'get_empty_tags', 'get_organizers_tags_item_id', 'put_organizers_tags_item_id', 'delete_recipe_tag', 'get_organizers_tags_slug_tag_slug', 'get_organizerss', 'post_organizerss', 'get_organizerss_item_id', 'put_organizerss_item_id', 'delete_organizerss_item_id', 'get_organizerss_slug_slug"
        )


def register_shared_tools(mcp: FastMCP):
    @mcp.tool(tags={"shared"})
    async def mealie_shared(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_shared_recipes', 'post_shared_recipes', 'get_shared_recipes_item_id', 'delete_shared_recipes_item_id'"
        ),
        recipe_id: Any | None = Field(default=None, description="recipe id"),
        accept_language: Any | None = Field(
            default=None, description="accept language"
        ),
        data: dict | None = Field(default=None, description="data"),
        item_id: str | None = Field(default=None, description="item id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage shared operations.

        Actions:
          - 'get_shared_recipes': Get All
          - 'post_shared_recipes': Create One
          - 'get_shared_recipes_item_id': Get One
          - 'delete_shared_recipes_item_id': Delete One
        """
        kwargs: dict[str, Any]
        if action == "get_shared_recipes":
            kwargs = {
                "recipe_id": recipe_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_shared_recipes(**kwargs)
        if action == "post_shared_recipes":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_shared_recipes(**kwargs)
        if action == "get_shared_recipes_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_shared_recipes_item_id(**kwargs)
        if action == "delete_shared_recipes_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_shared_recipes_item_id(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_shared_recipes', 'post_shared_recipes', 'get_shared_recipes_item_id', 'delete_shared_recipes_item_id"
        )


def register_admin_tools(mcp: FastMCP):
    @mcp.tool(tags={"admin"})
    async def mealie_admin(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_app_info', 'get_app_statistics', 'check_app_config', 'get_admin_users', 'post_admin_users', 'unlock_users', 'get_admin_users_item_id', 'put_admin_users_item_id', 'delete_admin_users_item_id', 'generate_token', 'get_admin_households', 'post_admin_households', 'get_admin_households_item_id', 'put_admin_households_item_id', 'delete_admin_households_item_id', 'get_admin_groups', 'post_admin_groups', 'get_admin_groups_item_id', 'put_admin_groups_item_id', 'delete_admin_groups_item_id', 'check_email_config', 'send_test_email', 'get_admin_backups', 'post_admin_backups', 'get_admin_backups_file_name', 'delete_admin_backups_file_name', 'upload_one', 'import_one', 'get_maintenance_summary', 'get_storage_details', 'clean_images', 'clean_temp', 'clean_recipe_folders', 'debug_openai'"
        ),
        accept_language: Any | None = Field(
            default=None, description="accept language"
        ),
        order_by: Any | None = Field(default=None, description="order by"),
        order_by_null_position: Any | None = Field(
            default=None, description="order by null position"
        ),
        order_direction: Any | None = Field(
            default=None, description="order direction"
        ),
        query_filter: Any | None = Field(default=None, description="query filter"),
        pagination_seed: Any | None = Field(
            default=None, description="pagination seed"
        ),
        page: int | None = Field(default=None, description="page"),
        per_page: int | None = Field(default=None, description="per page"),
        data: Any | None = Field(default=None, description="data"),
        force: bool | None = Field(default=None, description="force"),
        item_id: str | None = Field(default=None, description="item id"),
        file_name: str | None = Field(default=None, description="file name"),
        client=Depends(get_client),
    ) -> dict:
        """Manage admin operations.

        Actions:
          - 'get_app_info': Get App Info
          - 'get_app_statistics': Get App Statistics
          - 'check_app_config': Check App Config
          - 'get_admin_users': Get All
          - 'post_admin_users': Create One
          - 'unlock_users': Unlock Users
          - 'get_admin_users_item_id': Get One
          - 'put_admin_users_item_id': Update One
          - 'delete_admin_users_item_id': Delete One
          - 'generate_token': Generate Token
          - 'get_admin_households': Get All
          - 'post_admin_households': Create One
          - 'get_admin_households_item_id': Get One
          - 'put_admin_households_item_id': Update One
          - 'delete_admin_households_item_id': Delete One
          - 'get_admin_groups': Get All
          - 'post_admin_groups': Create One
          - 'get_admin_groups_item_id': Get One
          - 'put_admin_groups_item_id': Update One
          - 'delete_admin_groups_item_id': Delete One
          - 'check_email_config': Check Email Config
          - 'send_test_email': Send Test Email
          - 'get_admin_backups': Get All
          - 'post_admin_backups': Create One
          - 'get_admin_backups_file_name': Get One
          - 'delete_admin_backups_file_name': Delete One
          - 'upload_one': Upload One
          - 'import_one': Import One
          - 'get_maintenance_summary': Get Maintenance Summary
          - 'get_storage_details': Get Storage Details
          - 'clean_images': Clean Images
          - 'clean_temp': Clean Temp
          - 'clean_recipe_folders': Clean Recipe Folders
          - 'debug_openai': Debug Openai
        """
        kwargs: dict[str, Any]
        if action == "get_app_info":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_app_info(**kwargs)
        if action == "get_app_statistics":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_app_statistics(**kwargs)
        if action == "check_app_config":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.check_app_config(**kwargs)
        if action == "get_admin_users":
            kwargs = {
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_admin_users(**kwargs)
        if action == "post_admin_users":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_admin_users(**kwargs)
        if action == "unlock_users":
            kwargs = {
                "force": force,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.unlock_users(**kwargs)
        if action == "get_admin_users_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_admin_users_item_id(**kwargs)
        if action == "put_admin_users_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_admin_users_item_id(**kwargs)
        if action == "delete_admin_users_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_admin_users_item_id(**kwargs)
        if action == "generate_token":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.generate_token(**kwargs)
        if action == "get_admin_households":
            kwargs = {
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_admin_households(**kwargs)
        if action == "post_admin_households":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_admin_households(**kwargs)
        if action == "get_admin_households_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_admin_households_item_id(**kwargs)
        if action == "put_admin_households_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_admin_households_item_id(**kwargs)
        if action == "delete_admin_households_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_admin_households_item_id(**kwargs)
        if action == "get_admin_groups":
            kwargs = {
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_admin_groups(**kwargs)
        if action == "post_admin_groups":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_admin_groups(**kwargs)
        if action == "get_admin_groups_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_admin_groups_item_id(**kwargs)
        if action == "put_admin_groups_item_id":
            kwargs = {
                "item_id": item_id,
                "data": data,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.put_admin_groups_item_id(**kwargs)
        if action == "delete_admin_groups_item_id":
            kwargs = {
                "item_id": item_id,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_admin_groups_item_id(**kwargs)
        if action == "check_email_config":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.check_email_config(**kwargs)
        if action == "send_test_email":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.send_test_email(**kwargs)
        if action == "get_admin_backups":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_admin_backups(**kwargs)
        if action == "post_admin_backups":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.post_admin_backups(**kwargs)
        if action == "get_admin_backups_file_name":
            kwargs = {
                "file_name": file_name,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_admin_backups_file_name(**kwargs)
        if action == "delete_admin_backups_file_name":
            kwargs = {
                "file_name": file_name,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_admin_backups_file_name(**kwargs)
        if action == "upload_one":
            kwargs = {"data": data, "accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.upload_one(**kwargs)
        if action == "import_one":
            kwargs = {
                "file_name": file_name,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.import_one(**kwargs)
        if action == "get_maintenance_summary":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_maintenance_summary(**kwargs)
        if action == "get_storage_details":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_storage_details(**kwargs)
        if action == "clean_images":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.clean_images(**kwargs)
        if action == "clean_temp":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.clean_temp(**kwargs)
        if action == "clean_recipe_folders":
            kwargs = {"accept_language": accept_language}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.clean_recipe_folders(**kwargs)
        if action == "debug_openai":
            kwargs = {"accept_language": accept_language, "data": data}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.debug_openai(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_app_info', 'get_app_statistics', 'check_app_config', 'get_admin_users', 'post_admin_users', 'unlock_users', 'get_admin_users_item_id', 'put_admin_users_item_id', 'delete_admin_users_item_id', 'generate_token', 'get_admin_households', 'post_admin_households', 'get_admin_households_item_id', 'put_admin_households_item_id', 'delete_admin_households_item_id', 'get_admin_groups', 'post_admin_groups', 'get_admin_groups_item_id', 'put_admin_groups_item_id', 'delete_admin_groups_item_id', 'check_email_config', 'send_test_email', 'get_admin_backups', 'post_admin_backups', 'get_admin_backups_file_name', 'delete_admin_backups_file_name', 'upload_one', 'import_one', 'get_maintenance_summary', 'get_storage_details', 'clean_images', 'clean_temp', 'clean_recipe_folders', 'debug_openai"
        )


def register_explore_tools(mcp: FastMCP):
    @mcp.tool(tags={"explore"})
    async def mealie_explore(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_explore_groups_group_slug_foods', 'get_explore_groups_group_slug_foods_item_id', 'get_explore_groups_group_slug_households', 'get_household', 'get_explore_groups_group_slug_organizers_categories', 'get_explore_groups_group_slug_organizers_categories_item_id', 'get_explore_groups_group_slug_organizers_tags', 'get_explore_groups_group_slug_organizers_tags_item_id', 'get_explore_groups_group_slug_organizerss', 'get_explore_groups_group_slug_organizerss_item_id', 'get_explore_groups_group_slug_cookbooks', 'get_explore_groups_group_slug_cookbooks_item_id', 'get_explore_groups_group_slug_recipes', 'get_explore_groups_group_slug_recipes_suggestions', 'get_recipe'"
        ),
        group_slug: str | None = Field(default=None, description="group slug"),
        search: Any | None = Field(default=None, description="search"),
        order_by: Any | None = Field(default=None, description="order by"),
        order_by_null_position: Any | None = Field(
            default=None, description="order by null position"
        ),
        order_direction: Any | None = Field(
            default=None, description="order direction"
        ),
        query_filter: Any | None = Field(default=None, description="query filter"),
        pagination_seed: Any | None = Field(
            default=None, description="pagination seed"
        ),
        page: int | None = Field(default=None, description="page"),
        per_page: int | None = Field(default=None, description="per page"),
        accept_language: Any | None = Field(
            default=None, description="accept language"
        ),
        item_id: Any | None = Field(default=None, description="item id"),
        household_slug: str | None = Field(default=None, description="household slug"),
        categories: Any | None = Field(default=None, description="categories"),
        tags: Any | None = Field(default=None, description="tags"),
        tools: Any | None = Field(default=None, description="tools"),
        foods: Any | None = Field(default=None, description="foods"),
        households: Any | None = Field(default=None, description="households"),
        cookbook: Any | None = Field(default=None, description="cookbook"),
        require_all_categories: bool | None = Field(
            default=None, description="require all categories"
        ),
        require_all_tags: bool | None = Field(
            default=None, description="require all tags"
        ),
        require_all_tools: bool | None = Field(
            default=None, description="require all tools"
        ),
        require_all_foods: bool | None = Field(
            default=None, description="require all foods"
        ),
        limit: int | None = Field(default=None, description="limit"),
        max_missing_foods: int | None = Field(
            default=None, description="max missing foods"
        ),
        max_missing_tools: int | None = Field(
            default=None, description="max missing tools"
        ),
        include_foods_on_hand: bool | None = Field(
            default=None, description="include foods on hand"
        ),
        include_tools_on_hand: bool | None = Field(
            default=None, description="include tools on hand"
        ),
        recipe_slug: str | None = Field(default=None, description="recipe slug"),
        client=Depends(get_client),
    ) -> dict:
        """Manage explore operations.

        Actions:
          - 'get_explore_groups_group_slug_foods': Get All
          - 'get_explore_groups_group_slug_foods_item_id': Get One
          - 'get_explore_groups_group_slug_households': Get All
          - 'get_household': Get Household
          - 'get_explore_groups_group_slug_organizers_categories': Get All
          - 'get_explore_groups_group_slug_organizers_categories_item_id': Get One
          - 'get_explore_groups_group_slug_organizers_tags': Get All
          - 'get_explore_groups_group_slug_organizers_tags_item_id': Get One
          - 'get_explore_groups_group_slug_organizerss': Call get_explore_groups_group_slug_organizerss
          - 'get_explore_groups_group_slug_organizerss_item_id': Call get_explore_groups_group_slug_organizerss_item_id
          - 'get_explore_groups_group_slug_cookbooks': Get All
          - 'get_explore_groups_group_slug_cookbooks_item_id': Get One
          - 'get_explore_groups_group_slug_recipes': Get All
          - 'get_explore_groups_group_slug_recipes_suggestions': Suggest Recipes
          - 'get_recipe': Get Recipe
        """
        kwargs: dict[str, Any]
        if action == "get_explore_groups_group_slug_foods":
            kwargs = {
                "group_slug": group_slug,
                "search": search,
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_explore_groups_group_slug_foods(**kwargs)
        if action == "get_explore_groups_group_slug_foods_item_id":
            kwargs = {
                "item_id": item_id,
                "group_slug": group_slug,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_explore_groups_group_slug_foods_item_id(**kwargs)
        if action == "get_explore_groups_group_slug_households":
            kwargs = {
                "group_slug": group_slug,
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_explore_groups_group_slug_households(**kwargs)
        if action == "get_household":
            kwargs = {
                "household_slug": household_slug,
                "group_slug": group_slug,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_household(**kwargs)
        if action == "get_explore_groups_group_slug_organizers_categories":
            kwargs = {
                "group_slug": group_slug,
                "search": search,
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_explore_groups_group_slug_organizers_categories(**kwargs)
        if action == "get_explore_groups_group_slug_organizers_categories_item_id":
            kwargs = {
                "item_id": item_id,
                "group_slug": group_slug,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_explore_groups_group_slug_organizers_categories_item_id(
                **kwargs
            )
        if action == "get_explore_groups_group_slug_organizers_tags":
            kwargs = {
                "group_slug": group_slug,
                "search": search,
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_explore_groups_group_slug_organizers_tags(**kwargs)
        if action == "get_explore_groups_group_slug_organizers_tags_item_id":
            kwargs = {
                "item_id": item_id,
                "group_slug": group_slug,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_explore_groups_group_slug_organizers_tags_item_id(
                **kwargs
            )
        if action == "get_explore_groups_group_slug_organizerss":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_explore_groups_group_slug_organizerss(**kwargs)
        if action == "get_explore_groups_group_slug_organizerss_item_id":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_explore_groups_group_slug_organizerss_item_id(**kwargs)
        if action == "get_explore_groups_group_slug_cookbooks":
            kwargs = {
                "group_slug": group_slug,
                "search": search,
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_explore_groups_group_slug_cookbooks(**kwargs)
        if action == "get_explore_groups_group_slug_cookbooks_item_id":
            kwargs = {
                "item_id": item_id,
                "group_slug": group_slug,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_explore_groups_group_slug_cookbooks_item_id(**kwargs)
        if action == "get_explore_groups_group_slug_recipes":
            kwargs = {
                "group_slug": group_slug,
                "categories": categories,
                "tags": tags,
                "tools": tools,
                "foods": foods,
                "households": households,
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "page": page,
                "per_page": per_page,
                "cookbook": cookbook,
                "require_all_categories": require_all_categories,
                "require_all_tags": require_all_tags,
                "require_all_tools": require_all_tools,
                "require_all_foods": require_all_foods,
                "search": search,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_explore_groups_group_slug_recipes(**kwargs)
        if action == "get_explore_groups_group_slug_recipes_suggestions":
            kwargs = {
                "group_slug": group_slug,
                "foods": foods,
                "tools": tools,
                "order_by": order_by,
                "order_by_null_position": order_by_null_position,
                "order_direction": order_direction,
                "query_filter": query_filter,
                "pagination_seed": pagination_seed,
                "limit": limit,
                "max_missing_foods": max_missing_foods,
                "max_missing_tools": max_missing_tools,
                "include_foods_on_hand": include_foods_on_hand,
                "include_tools_on_hand": include_tools_on_hand,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_explore_groups_group_slug_recipes_suggestions(**kwargs)
        if action == "get_recipe":
            kwargs = {
                "recipe_slug": recipe_slug,
                "group_slug": group_slug,
                "accept_language": accept_language,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_recipe(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_explore_groups_group_slug_foods', 'get_explore_groups_group_slug_foods_item_id', 'get_explore_groups_group_slug_households', 'get_household', 'get_explore_groups_group_slug_organizers_categories', 'get_explore_groups_group_slug_organizers_categories_item_id', 'get_explore_groups_group_slug_organizers_tags', 'get_explore_groups_group_slug_organizers_tags_item_id', 'get_explore_groups_group_slug_organizerss', 'get_explore_groups_group_slug_organizerss_item_id', 'get_explore_groups_group_slug_cookbooks', 'get_explore_groups_group_slug_cookbooks_item_id', 'get_explore_groups_group_slug_recipes', 'get_explore_groups_group_slug_recipes_suggestions', 'get_recipe"
        )


def register_utils_tools(mcp: FastMCP):
    @mcp.tool(tags={"utils"})
    async def mealie_utils(
        action: str = Field(
            description="Action to perform. Must be one of: 'download_file'"
        ),
        token: Any | None = Field(default=None, description="token"),
        client=Depends(get_client),
    ) -> dict:
        """Manage utils operations.

        Actions:
          - 'download_file': Download File
        """
        kwargs: dict[str, Any]
        if action == "download_file":
            kwargs = {"token": token}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.download_file(**kwargs)
        raise ValueError(f"Unknown action: {action}. Must be one of: download_file")


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance."""
    load_dotenv(find_dotenv())
    args, mcp, middlewares = create_mcp_server(
        name="mealie-mcp MCP",
        version=__version__,
        instructions="mealie-mcp MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

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

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
    mcp, args, middlewares = get_mcp_instance()
    print(f"mealie-mcp MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)

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
