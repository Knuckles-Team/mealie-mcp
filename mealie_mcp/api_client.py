#!/usr/bin/env python

from mealie_mcp.api.api_client_admin import Api as AdminApi
from mealie_mcp.api.api_client_app import Api as AppApi
from mealie_mcp.api.api_client_explore import Api as ExploreApi
from mealie_mcp.api.api_client_groups import Api as GroupsApi
from mealie_mcp.api.api_client_households import Api as HouseholdsApi
from mealie_mcp.api.api_client_organizer import Api as OrganizerApi
from mealie_mcp.api.api_client_recipes import Api as RecipesApi
from mealie_mcp.api.api_client_shared import Api as SharedApi
from mealie_mcp.api.api_client_users import Api as UsersApi
from mealie_mcp.api.api_client_utils import Api as UtilsApi


class Api(
    AppApi,
    UsersApi,
    HouseholdsApi,
    GroupsApi,
    RecipesApi,
    OrganizerApi,
    SharedApi,
    AdminApi,
    ExploreApi,
    UtilsApi,
):
    pass
