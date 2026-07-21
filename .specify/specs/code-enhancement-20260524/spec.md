# Code Enhancement: mealie-mcp

> Automated code enhancement review for mealie-mcp. Covers 17 analysis domains.

## User Stories

- As a **developer**, I want to **address Project Analysis findings (grade: C, score: 74)**, so that **improve project project analysis from C to at least B (80+)**.
- As a **developer**, I want to **address Codebase Optimization findings (grade: F, score: 59)**, so that **improve project codebase optimization from F to at least B (80+)**.
- As a **developer**, I want to **address Test Coverage findings (grade: F, score: 55)**, so that **improve project test coverage from F to at least B (80+)**.
- As a **developer**, I want to **address Architecture & Design Patterns findings (grade: D, score: 65)**, so that **improve project architecture & design patterns from D to at least B (80+)**.
- As a **developer**, I want to **address Concept Traceability findings (grade: F, score: 29)**, so that **improve project concept traceability from F to at least B (80+)**.
- As a **developer**, I want to **address Test Execution findings (grade: F, score: 25)**, so that **improve project test execution from F to at least B (80+)**.
- As a **developer**, I want to **address Changelog Audit findings (grade: C, score: 75)**, so that **improve project changelog audit from C to at least B (80+)**.
- As a **developer**, I want to **address Environment Variables findings (grade: D, score: 62)**, so that **improve project environment variables from D to at least B (80+)**.
- As a **developer**, I want to **address analyze_xdg_kg findings (grade: F, score: 0)**, so that **improve project analyze_xdg_kg from F to at least B (80+)**.

## Functional Requirements

- **FR-001**: Minor update: agent-utilities 0.2.40 (installed) -> 0.16.0
- **FR-002**: Minor update: pytest-xdist 3.6.0 (constraint — not installed) -> 3.8.0
- **FR-003**: 32 functions exceed 50 lines
- **FR-004**: Monolithic: mcp_server.py (895L) — 7 functions with high complexity (worst: register_households_tools at 155L, CC=68); Low cohesion: 13 distinct concepts in one file
- **FR-005**: Monolithic: api_client_recipes.py (688L) — 1 functions with high complexity (worst: Api.get_recipes at 61L, CC=19); God class: Api (64 methods) — consider mixins/composition
- **FR-006**: Needs attention: api_client_households.py (827L) — God class: Api (64 methods) — consider mixins/composition
- **FR-007**: Low test-to-source ratio: 0.21
- **FR-008**: Test suite lacks intent diversity (only one type)
- **FR-009**: 15 potential doc-test drift items
- **FR-010**: README.md missing sections: usage|quick start
- **FR-011**: 2 broken internal links in README.md
- **FR-012**: README missing: Has a Table of Contents
- **FR-013**: README missing: Has usage examples with code blocks
- **FR-014**: SRP: 3 modules exceed 500 lines (god modules)
- **FR-015**: SRP: 6 classes have >15 methods
- **FR-016**: No discernible layer architecture (no domain/service/adapter separation)
- **FR-017**: Low dependency injection ratio: 8%
- **FR-018**: Low traceability ratio: 0% concepts fully traced
- **FR-019**: 18 orphaned concepts (only in one source)
- **FR-020**: 8 test functions missing concept markers
- **FR-021**: 114 significant functions (>10 lines) missing concept markers in docstrings
- **FR-022**: Total lint findings: 0 (high/error: 0, medium/warning: 0, low: 0)
- **FR-023**: 2 hook(s) may be outdated: ruff-pre-commit, uv-pre-commit
- **FR-024**: 1 rogue/throwaway scripts detected (fix_*, validate_*, patch_*, etc.): scripts/validate_a2a_agent.py
- **FR-025**: CHANGELOG.md exists but could not be parsed — check format compliance
- **FR-026**: No changelog entries within the last 30 days
- **FR-027**: keepachangelog not installed — pip install 'universal-skills[code-enhancer]'
- **FR-028**: 3 tests have no assertions
- **FR-029**: Only 25% of env vars documented in README.md
- **FR-030**: Undocumented env vars: ADMINTOOL, APPTOOL, AUTH_TYPE, DEFAULT_AGENT_NAME, EUNOMIA_POLICY_FILE, EUNOMIA_TYPE, EXPLORETOOL, GROUPSTOOL, HOUSEHOLDSTOOL, MEALIE_BASE_URL
- **FR-031**: Runtime connection configuration must document DEFAULT_AGENT_NAME, MEALIE_BASE_URL, MEALIE_TOKEN, and the AgentConfig TLS profile references.
- **FR-032**: Analysis error: No module named 'agent_utilities.knowledge_graph'

## Success Criteria

- Overall GPA: 2.18 → 3.0
- Domains at B or above: 8 → 17
- Actionable findings: 32 → 0
