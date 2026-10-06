"""Generate typed recipe inputs from the checked-in upstream OpenAPI subset."""

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _canonical_date_aliases(schemas):
    """Use Mealie's accepted response spelling for its date alias."""
    # Mealie accepts update_at/updateAt/updated_at/updatedAt via AliasChoices.
    # Advertise the canonical response spelling so lookup records round-trip.
    for schema in schemas.values():
        properties = schema.get("properties", {})
        if "update_at" in properties:
            properties["updatedAt"] = properties.pop("update_at")
            if "update_at" in schema.get("required", []):
                schema["required"] = [
                    "updatedAt" if field == "update_at" else field
                    for field in schema["required"]
                ]


def generate():
    """Apply semantic descriptions, then use the standard Pydantic generator."""
    document = json.loads((ROOT / "schemas/recipe-inputs.openapi.json").read_text())
    schemas = document["components"]["schemas"]
    schemas.pop("HTTPValidationError")
    schemas.pop("ValidationError")
    ingredient = schemas["RecipeIngredient"]["properties"]
    ingredient["title"]["description"] = (
        "Ingredient section heading (for example Sauce), not the ingredient text. "
        "Use food, note and originalText for the ingredient itself."
    )
    for noun in ("Food", "Unit"):
        ingredient[noun.lower()]["description"] = (
            f"An existing Ingredient{noun} record from lookup, or a "
            f"CreateIngredient{noun} object. A bare ID is not accepted."
        )
    _canonical_date_aliases(schemas)
    for schema in schemas.values():
        for field in schema.get("properties", {}).values():
            field.pop("title", None)
    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "recipe-inputs.openapi.json"
        source.write_text(json.dumps(document))
        subprocess.run(
            [
                "datamodel-codegen",
                "--input",
                str(source),
                "--input-file-type",
                "openapi",
                "--output-model-type",
                "pydantic_v2.BaseModel",
                "--output",
                str(ROOT / "mealie_mcp/recipe_models.py"),
                "--target-python-version",
                "3.12",
                "--disable-timestamp",
                "--use-standard-collections",
                "--use-union-operator",
                "--field-constraints",
                "--strict-nullable",
                "--strict-types",
                "str",
                "int",
                "float",
                "bool",
                "--formatters",
                "ruff-check",
                "ruff-format",
                "--extra-fields",
                "forbid",
                "--use-generic-base-class",
            ],
            check=True,
        )


if __name__ == "__main__":
    generate()
