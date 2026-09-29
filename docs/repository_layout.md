# Repository layout (CortexOT)

| Path | Role |
|------|------|
| [`app/`](../app/) | Backend (`cortexot-backend`) — see [clean_architecture.md](clean_architecture.md) |
| [`cortexot_plant/`](../cortexot_plant/) | Shared `/Plant` tag definitions (backend + simulator) |
| [`simulator/`](../simulator/) | OPC-UA + HTTP demo (`cortexot-simulator`) |
| [`mcp/`](../mcp/) | Industrial MCP placeholder (Phase 3+) |
| [`alembic/`](../alembic/) | DB migrations |
| [`docker/`](../docker/) | Dockerfiles and Timescale init |
| [`docs/`](../docs/) | Architecture and runbooks |
| [`tests/`](../tests/) | Pytest |
| [`.github/workflows/`](../.github/workflows/) | CI (Snyk Code) |

New top-level packages (e.g. analytics) are added **when implementation starts**, not as empty placeholders.

Local-only: `.venv/`, `__pycache__/`, `.pytest_cache/` (see [`.gitignore`](../.gitignore)).
