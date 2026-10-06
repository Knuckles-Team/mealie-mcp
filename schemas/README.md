# Recipe input schema provenance

`recipe-inputs.openapi.json` is a bounded OpenAPI export from the unmodified
[Mealie v3.28.0 source](https://github.com/mealie-recipes/mealie/tree/0552eaa4a80031b8572849cca0ed95d07f1be001)
(commit `0552eaa4a80031b8572849cca0ed95d07f1be001`). It includes only the
CreateRecipe, Recipe, CreateIngredientFood and CreateIngredientUnit request
models and their transitive references. The five native request-body bindings
are verified against the upstream recipe, food and unit routes. It is not a
copy of the entire API or a schema retrieved from a personal Mealie server.
The checked-in export SHA-256 is
`5c096ef35d938e5cbabf7e40961fbbf1bdca1419924989ac27831cb5d524bc45`.

Mealie does not check in a release OpenAPI document. `scripts/export_recipe_schema.py`
uses FastAPI to export the release's actual Python request models into a minimal
OpenAPI document. Its functions are schema-only endpoints; no Mealie service,
database, credentials or meal data is used. Export with the upstream checkout on
PYTHONPATH in a Python 3.14 environment with its pinned dependencies, including
FastAPI 0.141.1 and Pydantic 2.13.5:

```sh
PYTHONPATH=/path/to/pinned/mealie PRODUCTION=true DATA_DIR=/tmp/mealie-schema-data \
  python scripts/export_recipe_schema.py schemas/recipe-inputs.openapi.json
```

Generate `mealie_mcp/recipe_models.py` using datamodel-code-generator 0.83.0 and
Ruff 0.15.12 on Python 3.12:

```sh
uv run --no-project --python 3.12 \
  --with 'datamodel-code-generator[ruff]==0.83.0' --with ruff==0.15.12 \
  python scripts/generate_recipe_models.py
```

The generator uses the standard OpenAPI/Pydantic parser, not a connector-local
schema interpreter. The generated module is committed, so server startup needs
neither upstream Mealie nor code-generation packages or network access.

## Deliberate overlays and limits

- Describe `RecipeIngredient.title` as the ingredient section heading.
- Describe food/unit as existing-record or create-record objects, not bare IDs.
- Advertise `updatedAt`, Mealie's canonical response spelling, for its
  `update_at` field. Upstream accepts both through `AliasChoices`; this lets
  lookup records round-trip through typed inputs.
- Drop redundant upstream field-title metadata during generation; Pydantic supplies
  display titles automatically. Field names and structure remain unchanged.
- Forbid unknown model fields and use strict primitive types to catch typos and
  malformed nested values before invoking the API. Open `extras` dictionaries
  remain open. This is intentionally stricter than Mealie's coercion behavior;
  the existing `params_json` surface remains unchanged.
- Validate recipe path slugs at the shared client boundary and in typed inputs.
  Reject path separators, query/fragment delimiters, controls and dot segments,
  including repeatedly percent-encoded forms, before any request. Encode accepted
  identifiers as one path segment. Explicit Mealie slugs are not necessarily
  slugified; Unicode, spaces and ordinary punctuation remain supported.

Upstream Python validators (for example slug normalization and substitution
business rules) are not represented by OpenAPI and remain server-side. Generated
optional fields without an OpenAPI default may accept null in addition to
omission. UUIDs, required fields, nested object/list structure and primitive types
are validated locally. Both PUT and PATCH use upstream Recipe; no invented
partial model or silent composite creation is introduced. Serialization excludes
unset fields, including nested defaults, while preserving explicit nulls.

To update, review the new release's request-body bindings, export again from the
new pinned commit, regenerate, run the recipe contract tests and review the
schema diff. Do not hand-edit the generated models.
