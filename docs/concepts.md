# Concept Registry — mealie-mcp

> **Prefix**: `CONCEPT:MEAL-*`
> **Version**: 0.15.0
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

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:AU-ECO.messaging.native-backend-abstraction` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:AU-ORCH.adapter.hot-cache-invalidation` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:AU-OS.config.secrets-authentication` | Prompt Injection Defense | agent-utilities |
| `CONCEPT:AU-OS.state.cognitive-scheduler-preemption` | Cognitive Scheduler | agent-utilities |
| `CONCEPT:AU-OS.governance.reactive-multi-axis-budget` | Guardrail Engine | agent-utilities |
| `CONCEPT:AU-OS.governance.wasm-micro-agent-sandbox` | Audit Logging | agent-utilities |
| `CONCEPT:AU-KG.query.object-graph-mapper` | Knowledge Graph Core | agent-utilities |

## Synergy with agent-utilities

This project integrates with `agent-utilities` via `CONCEPT:AU-ECO.messaging.native-backend-abstraction` (Unified Toolkit Ingestion). The `mealie_mcp` MCP server registers its tools with the agent-utilities FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all MEAL-* concepts.
