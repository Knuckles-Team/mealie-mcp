---
name: mealie-mcp-development
skill_type: skill
description: >-
  Develop and verify mealie-mcp as a connector-owned package while preserving its
  SDK entry point, action-routed tool surface, authentication boundary, packaged
  content, and source-backed spec-delivery publication.
---

# Mealie MCP Development

Use this skill for changes to the `mealie-mcp` connector package. The package is
the connector for a Mealie HTTP API; it does not own the SDK, Arbora admission,
the central Pages renderer, or generated container/Compose output.

## Repository map and runtime boundary

- `mealie_mcp/__init__.py` creates the SDK `Connector` with
  `mealie_mcp.mcp_server` as its tool module.
- `mealie_mcp/mcp_server.py` registers the action-routed FastMCP tools for the
  `app`, `users`, `households`, `groups`, `recipes`, `organizer`, `shared`,
  `admin`, `explore`, `utils`, and `kg` domains. The `mealie_mcp/mcp/` modules
  are retained source mirrors; the connector wiring above is the active import.
- `mealie_mcp/api_client.py` combines the domain clients in `mealie_mcp/api/`.
  `mealie_mcp/auth.py` creates the API client from runtime settings and resolves
  the SDK TLS profile named `mealie`.
- `mealie_mcp/ontology/`, `mealie_mcp/prompts/`, and
  `mealie_mcp/skills/` are packaged connector content. `pyproject.toml` keeps
  their `skills/**`, `ontology/**`, `prompts/**`, and `mcp_config.json` data.
- The only declared console script is `mealie-mcp`, provided by
  `scion_sdk.cli:serve`. `python -m mealie_mcp` delegates to the SDK
  runner through `mealie_mcp/__main__.py`. Do not invent a second agent entry
  point: the current `pyproject.toml` declares no `mealie-agent` script.

The connector reads `MEALIE_BASE_URL` and `MEALIE_TOKEN` through the SDK setting
boundary. `MEALIE_TLS_PROFILE` and `MEALIE_TLS_PROFILE_REF` select runtime TLS
trust when configured. Tool toggles and transport flags are launcher settings;
keep credentials, hostnames, and TLS material out of source, skills, traces, and
MCP client configuration committed to the repository.

## Rapid delivery: the 5-minute contract

1. Read the owning `specs/` row and the applicable `AGENTS.md` before editing.
2. Inspect the active source path and its focused tests before changing a tool,
   auth seam, ontology artifact, or packaged skill.
3. Prefer the smallest connector-owned change. Preserve action names, parameter
   schemas, SDK `Connector` wiring, auth/TLS verification, and package-data
   declarations unless the owning requirement explicitly changes them.
4. Run the focused tests through the narrow test-slot wrapper, then run the
   repository pre-commit and pre-push gates without bypasses.
5. For a public payload change, update the package version and `uv.lock`
   coherently. Inspect the built wheel for the new packaged content.
6. Treat the Pages site as a separate proof: after the exact main revision has a
   successful `pages.yml` run, check `/spec-delivery/`, its `index.html`, and
   `snapshot.json` over HTTPS. Record the exact revision from the snapshot.

## Focused development commands

From the repository root:

```bash
uv sync --locked

/var/tmp/arbora-delivery/scale/run-narrow-test-slot.sh \
  uv run --locked --extra test pytest -q \
    tests/test_init.py \
    tests/test_init_dynamics.py \
    tests/test_action_discovery.py \
    tests/test_recipe_paths.py \
    tests/test_recipe_tools.py \
    tests/test_publication_workflow.py

uvx pre-commit run --all-files
uvx pre-commit run --all-files --hook-stage pre-push
```

The focused tests cover SDK server construction, package metadata, action
discovery, recipe routing, and the Pages/release contract. Use the existing
characterization tests when changing the corresponding dispatch behavior. Do
not replace these checks with a live Mealie call or a credential-bearing test.

## Pages and package publication

`.github/workflows/pages.yml` is the one Pages caller. It invokes the shared
Pipelines `pages_pipeline.yml@main` with `content_source: docs` and the version 1
`.github/spec-dashboard.json` source declaration for `specs/*/status.json`.
Keep both manual dispatch and the `docs/**`, `mkdocs.yml`, `README.md`, `specs/**`,
config, and workflow path filters. The old direct `mkdocs gh-deploy` publisher
must not be restored because it would compete with the shared dashboard build.

After a merge, verify the exact main SHA in the successful Pages run and probe:

```bash
curl -fsSI https://knuckles-team.github.io/mealie-mcp/
curl -fsSI https://knuckles-team.github.io/mealie-mcp/spec-delivery/
curl -fsSI https://knuckles-team.github.io/mealie-mcp/spec-delivery/index.html
curl -fsS https://knuckles-team.github.io/mealie-mcp/spec-delivery/snapshot.json
```

Use the shared `connector: true` and `render_connector: true` pipeline flags in
`.github/workflows/pipeline.yml`. Central generation owns connector manifests and
container/Compose artifacts; this repository currently has no product Dockerfile
or Compose runtime to duplicate locally. Keep generated renderer output outside
the checkout and report its pinned provider revision with the review evidence.

## Change discipline

- Keep Mealie API calls, request models, ontology mappings, and MCP schemas under
  this repository's `CONN-MEALIE-MCP-*` boundary. SDK transport and central
  renderer behavior belong to their owner repositories.
- Use `MEALIE_BASE_URL` and `MEALIE_TOKEN` only in an injected runtime environment;
  never print or commit their values. Preserve certificate verification and the
  named TLS profile path.
- For mutations, begin with a read or discovery action, require operator approval,
  and verify the result. Keep KG ingestion opt-in and follow its existing
  provenance/tenant contract.
- Keep generated status changes and central publication promotion with the
  pipelines/status owner. Do not claim a Pages or public package result from a
  local build.
