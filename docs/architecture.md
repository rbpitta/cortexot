# CortexOT architecture

**Product:** CortexOT — Industrial AI Advisor  
**Repository:** `cortexot`

Phase 0 establishes containers and health checks only. The approved target architecture:

1. `cortexot-simulator` exposes OPC-UA `/Plant/*` and `/AI/*` (Phase 1+).
2. `cortexot-backend` subscribes to process tags, runs analytics and agent orchestration.
3. **Industrial MCP** (`cortexot-mcp`) exposes read-only tools to the agent.
4. `cortexot-ollama` runs the local LLM.
5. Recommendations publish to `/AI/*` only; operator feedback via `/AI/.../Feedback/*`.

Detailed contracts will live in `docs/opcua_contract.md` (Phase 5).

## Git workflow

CortexOT uses a simple integration flow aligned with Jira feature branches:

| Branch | Purpose |
|--------|---------|
| `main` | Production / stable releases only |
| `develop` | Integration branch for the PoC |
| `feature/<JIRA-ID>-<short-description>` | Implementation work tied to a Jira issue (e.g. `feature/SCRUM-27-pump-telemetry`) |

**Expected flow:**

1. Branch from `develop` using the Jira key in the branch name.
2. Open a pull request into `develop` when the issue acceptance criteria are met.
3. After release validation on `develop`, open a pull request from `develop` into `main`.

Do not commit secrets (`.env` stays local; use `.env.example` as the template).
