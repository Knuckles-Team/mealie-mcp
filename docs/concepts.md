# Concept Registry — mealie-mcp

> **Prefix**: `CONCEPT:MEAL-*`
> **Version**: 0.15.0
> **Bridge**: [`CONCEPT:ECO-4.0`](../../agent-utilities/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:MEAL-001` | Administration | MCP tool domain `admin` — Action-routed dynamic tool registration |
| `CONCEPT:MEAL-002` | App Operations | MCP tool domain `app` — Action-routed dynamic tool registration |
| `CONCEPT:MEAL-003` | Explore Operations | MCP tool domain `explore` — Action-routed dynamic tool registration |
| `CONCEPT:MEAL-004` | Group Management | MCP tool domain `groups` — Action-routed dynamic tool registration |
| `CONCEPT:MEAL-005` | Households Operations | MCP tool domain `households` — Action-routed dynamic tool registration |
| `CONCEPT:MEAL-006` | Organizer Operations | MCP tool domain `organizer` — Action-routed dynamic tool registration |
| `CONCEPT:MEAL-007` | Recipe Management | MCP tool domain `recipes` — Action-routed dynamic tool registration |
| `CONCEPT:MEAL-008` | Shared Operations | MCP tool domain `shared` — Action-routed dynamic tool registration |
| `CONCEPT:MEAL-009` | Users Operations | MCP tool domain `users` — Action-routed dynamic tool registration |
| `CONCEPT:MEAL-010` | Utils Operations | MCP tool domain `utils` — Action-routed dynamic tool registration |

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:ECO-4.0` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:ORCH-1.2` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:OS-5.1` | Prompt Injection Defense | agent-utilities |
| `CONCEPT:OS-5.2` | Cognitive Scheduler | agent-utilities |
| `CONCEPT:OS-5.3` | Guardrail Engine | agent-utilities |
| `CONCEPT:OS-5.4` | Audit Logging | agent-utilities |
| `CONCEPT:KG-2.0` | Knowledge Graph Core | agent-utilities |

## Synergy with agent-utilities

This project integrates with `agent-utilities` via `CONCEPT:ECO-4.0` (Unified Toolkit Ingestion). The `mealie_mcp` MCP server registers its tools with the agent-utilities FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all MEAL-* concepts.
