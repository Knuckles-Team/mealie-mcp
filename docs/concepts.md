# Concept Registry — mealie-mcp

> **Prefix**: `CONCEPT:MEAL-*`
> **Version**: 0.15.0
> **Bridge**: [`CONCEPT:AU-ECO.messaging.native-backend-abstraction`](https://knuckles-team.github.io/agent-connector-sdk/) (Unified Toolkit Ingestion)
> **Bridge**: `CONCEPT:AU-ECO.messaging.native-backend-abstraction` in the Agent Utilities concept registry (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:MK-OS.governance.meal` | Administration | MCP tool domain `admin` — Action-routed dynamic tool registration |
| `CONCEPT:MK-OS.governance.meal-2` | App Operations | MCP tool domain `app` — Action-routed dynamic tool registration |
| `CONCEPT:MK-OS.governance.meal-3` | Explore Operations | MCP tool domain `explore` — Action-routed dynamic tool registration |
| `CONCEPT:MK-OS.governance.meal-4` | Group Management | MCP tool domain `groups` — Action-routed dynamic tool registration |
| `CONCEPT:MK-OS.governance.meal-5` | Households Operations | MCP tool domain `households` — Action-routed dynamic tool registration |
| `CONCEPT:MK-OS.governance.meal-6` | Organizer Operations | MCP tool domain `organizer` — Action-routed dynamic tool registration |
| `CONCEPT:MK-OS.governance.meal-7` | Recipe Management | MCP tool domain `recipes` — Action-routed dynamic tool registration |
| `CONCEPT:MK-OS.governance.meal-8` | Shared Operations | MCP tool domain `shared` — Action-routed dynamic tool registration |
| `CONCEPT:MK-OS.governance.meal-9` | Users Operations | MCP tool domain `users` — Action-routed dynamic tool registration |
| `CONCEPT:MK-OS.governance.meal-10` | Utils Operations | MCP tool domain `utils` — Action-routed dynamic tool registration |

## Cross-Project References (from scion-sdk)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:AU-ECO.messaging.native-backend-abstraction` | Unified Toolkit Ingestion | scion-sdk |
| `CONCEPT:AU-ORCH.adapter.hot-cache-invalidation` | Confidence-Gated Router | scion-sdk |
| `CONCEPT:AU-OS.config.secrets-authentication` | Prompt Injection Defense | scion-sdk |
| `CONCEPT:AU-OS.state.cognitive-scheduler-preemption` | Cognitive Scheduler | scion-sdk |
| `CONCEPT:AU-OS.governance.reactive-multi-axis-budget` | Guardrail Engine | scion-sdk |
| `CONCEPT:AU-OS.governance.wasm-micro-agent-sandbox` | Audit Logging | scion-sdk |
| `CONCEPT:AU-KG.query.object-graph-mapper` | Knowledge Graph Core | scion-sdk |

## Synergy with scion-sdk

This project integrates with `scion-sdk` via `CONCEPT:AU-ECO.messaging.native-backend-abstraction` (Unified Toolkit Ingestion). The `mealie_mcp` MCP server registers its tools with the scion-sdk FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all MEAL-* concepts.
