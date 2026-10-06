"""Export the bounded OpenAPI schema using an unmodified pinned Mealie checkout.

Run in the upstream Python 3.14 environment; see schemas/README.md.
"""

import json
import sys
from pathlib import Path

from fastapi import FastAPI
from mealie.schema.recipe.recipe import CreateRecipe, Recipe
from mealie.schema.recipe.recipe_ingredient import (
    CreateIngredientFood,
    CreateIngredientUnit,
)

app = FastAPI(title="Mealie recipe write inputs", version="3.28.0")


def create(data: CreateRecipe):
    """Native initial creation body."""
    return data


def write(slug: str, data: Recipe):
    """Native update and patch body."""
    return data


def food(data: CreateIngredientFood):
    """Native food creation body."""
    return data


def unit(data: CreateIngredientUnit):
    """Native unit creation body."""
    return data


app.post("/api/recipes")(create)
app.put("/api/recipes/{slug}")(write)
app.patch("/api/recipes/{slug}")(write)
app.post("/api/foods")(food)
app.post("/api/units")(unit)
Path(sys.argv[1]).write_text(json.dumps(app.openapi(), indent=2) + "\n")
