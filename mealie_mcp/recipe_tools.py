"""Typed native recipe workflow, registered alongside the compatible action tool."""

from typing import Annotated, Any

from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from pydantic import AfterValidator, BaseModel, Field

from mealie_mcp.api.path_parameters import validate_recipe_slug
from mealie_mcp.auth import get_client
from mealie_mcp.recipe_models import (
    CreateIngredientFood,
    CreateIngredientUnit,
    CreateRecipe,
    Recipe,
)

Slug = Annotated[
    str,
    Field(
        min_length=1,
        description="Recipe slug returned by creation or lookup; a single safe URL path segment.",
    ),
    AfterValidator(validate_recipe_slug),
]


async def _write(client: Any, method: str, data: BaseModel, **path: str) -> Any:
    """Preserve omitted fields and explicit nulls; serialize UUID/date values."""
    return await run_blocking(
        getattr(client, method),
        data=data.model_dump(mode="json", by_alias=True, exclude_unset=True),
        **path,
    )


def add_recipe_write_tools(mcp: FastMCP):
    """Add typed tools under the recipes domain's existing visibility policy."""

    @mcp.tool(tags={"recipes", "typed"})
    async def mealie_recipe_create(
        data: CreateRecipe, client=Depends(get_client)
    ) -> Any:
        """Create a recipe with {name}; returns its slug. Then use mealie_recipe_update
        or mealie_recipe_patch to populate ingredients/instructions. This performs
        only the native POST /api/recipes, not a composite transaction.
        """
        return await _write(client, "post_recipes", data)

    @mcp.tool(tags={"recipes", "typed"})
    async def mealie_recipe_update(
        slug: Slug, data: Recipe, client=Depends(get_client)
    ) -> Any:
        """Replace a recipe via native PUT. Fetch the current recipe first, preserve
        its fields, then supply the edited body. Omitted fields may reset on Mealie.
        Ingredient title is a section heading. Find/create foods and units with
        mealie_recipe_foods/mealie_recipe_units and their create tools.
        """
        return await _write(client, "put_recipes_slug", data, slug=slug)

    @mcp.tool(tags={"recipes", "typed"})
    async def mealie_recipe_patch(
        slug: Slug, data: Recipe, client=Depends(get_client)
    ) -> Any:
        """Patch only supplied recipe fields via native PATCH. Lists such as
        recipeIngredient are supplied as a whole, not merged by ingredient ID.
        Omitted fields are not sent; explicit nulls are preserved.
        """
        return await _write(client, "patch_one", data, slug=slug)

    @mcp.tool(tags={"recipes", "typed"})
    async def mealie_recipe_food_create(
        data: CreateIngredientFood, client=Depends(get_client)
    ) -> Any:
        """Create a food record for recipe ingredients; look up existing foods first."""
        return await _write(client, "post_foods", data)

    @mcp.tool(tags={"recipes", "typed"})
    async def mealie_recipe_unit_create(
        data: CreateIngredientUnit, client=Depends(get_client)
    ) -> Any:
        """Create a unit record for recipe ingredients; look up existing units first."""
        return await _write(client, "post_units", data)

    @mcp.tool(tags={"recipes", "typed"})
    async def mealie_recipe_foods(
        *,
        search: str | None = None,
        page: int = 1,
        per_page: int = 50,
        client=Depends(get_client),
    ) -> Any:
        """Find existing food records by name; use the returned records in ingredient food."""
        return await run_blocking(
            client.get_foods, search=search, page=page, per_page=per_page
        )

    @mcp.tool(tags={"recipes", "typed"})
    async def mealie_recipe_units(
        *,
        search: str | None = None,
        page: int = 1,
        per_page: int = 50,
        client=Depends(get_client),
    ) -> Any:
        """Find existing unit records by name; use the returned records in ingredient unit."""
        return await run_blocking(
            client.get_units, search=search, page=page, per_page=per_page
        )
