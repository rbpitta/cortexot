# Repository layout (CortexOT)

Top-level folders under the monorepo and how they relate to Clean Architecture.

## Deployable services (separate processes in Docker Compose)

| Folder | Container | Role |
|--------|-----------|------|
| [`app/`](../app/) | `cortexot-backend` | FastAPI backend — **domain / application / infrastructure / presentation** (see [clean_architecture.md](clean_architecture.md)) |
| [`simulator/`](../simulator/) | `cortexot-simulator` | OPC-UA plant simulator + HTTP demo API |
| [`mcp/`](../mcp/) | `cortexot-mcp` | Industrial MCP placeholder (Phase 3+) |

## Shared libraries (Python packages in `pyproject.toml`)

| Folder | Used by |
|--------|---------|
| [`cortexot_plant/`](../cortexot_plant/) | Backend + simulator — `/Plant` tag names, thresholds, namespace URI (no `app → simulator` dependency) |

## Infrastructure & tooling (not application logic)

| Folder | Purpose |
|--------|---------|
| [`alembic/`](../alembic/) | Database migrations (Timescale / `cortexot` schema) |
| [`docker/`](../docker/) | Dockerfiles and DB init SQL |
| [`docs/`](../docs/) | Architecture, development, smoke checklists |
| [`tests/`](../tests/) | Pytest suite |
| [`.github/workflows/`](../.github/workflows/) | CI (e.g. Snyk Code) |

## Phase placeholders (empty until implemented)

These were reserved at Phase 0 for the modular monolith. **Do not** put Phase 1 OPC-UA code here; new code follows the same layering as `app/` (either inside `app/domain` + `app/application` or a new Hatch package when it becomes a separate deployable).

| Folder | Planned phase | Future content (indicative) |
|--------|---------------|-----------------------------|
| [`analytics/`](../analytics/) | Phase 2 | Anomaly detection, feature pipelines |
| [`agent/`](../agent/) | Phase 4 | Ollama orchestration, tool calling |
| [`recommendation/`](../recommendation/) | Phase 5 | Advisory payloads toward `/AI/*` |

Each folder currently contains only `.gitkeep` so Git tracks the directory.

## Removed / consolidated (Clean Architecture refactor)

| Old path | New location |
|----------|----------------|
| `integrations/opcua/` | `app/infrastructure/opcua/` |
| `models/db/` | `app/infrastructure/persistence/` |
| `app/api/`, `app/services/`, `app/workers/` | `app/presentation/` + `app/application/` + `app/infrastructure/` |

## Local-only (not committed)

- `.venv/`, `__pycache__/`, `.pytest_cache/` — see [`.gitignore`](../.gitignore)
