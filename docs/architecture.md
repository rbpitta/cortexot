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
