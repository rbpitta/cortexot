# CortexOT — Industrial AI Advisor

Headless Industrial AI platform integrated with SCADA/supervisory systems via **OPC-UA** (primary). This repository is a Proof of Concept evolving toward a production-grade advisor: collect process data, detect anomalies, investigate with a local LLM (Ollama) and **Industrial MCP** tools, and publish structured recommendations back to SCADA for operator acceptance.

**Phase 0** bootstrapped Docker, health checks, and placeholders. **Phase 1** adds OPC-UA plant telemetry (`/Plant/PUMP-01/*`), Timescale ingest, and a demo degradation scenario — still no LLM agent or real MCP tools.

## Stack

| Service | Container name | Role |
|---------|----------------|------|
| Backend | `cortexot-backend` | FastAPI API, future collectors & agent |
| Industrial MCP | `cortexot-mcp` | MCP tool layer (placeholder) |
| Simulator | `cortexot-simulator` | OPC-UA plant server + HTTP demo API |
| TimescaleDB | `cortexot-timescaledb` | PostgreSQL + TimescaleDB |
| Ollama | `cortexot-ollama` | Local LLM runtime |

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

Health endpoints:

- Backend: http://localhost:8000/health and http://localhost:8000/ready
- Industrial MCP: http://localhost:8001/health
- Simulator: http://localhost:8080/health (OPC-UA `opc.tcp://localhost:4840/cortexot/simulator/`)
- Ollama: http://localhost:11434/

Phase 1 demo (after stack is up):

```bash
curl -X POST http://localhost:8000/api/v1/demo/degradation/start \
  -H "Content-Type: application/json" \
  -d "{\"scenario\":\"bearing_degradation\"}"
```

Measurements land in `cortexot.measurements` (Timescale hypertable). Connect pgAdmin to `localhost:5432` (user/db/password `cortexot`).

## Local development

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
pytest
uvicorn app.main:app --reload --port 8000
```

## Architecture (approved)

- **OPC-UA primary** for `/Plant/*` (read) and `/AI/*` (advisory write allowlist) — Phase 1+
- **Industrial MCP**: single server (`cortexot-mcp`) with internal telemetry/knowledge/maintenance domains
- **Security**: LLM never writes to PLC; no autonomous control in PoC
- **MQTT**: optional future profile, not required for the main demo

See `docs/architecture.md` (expanded in later phases).

**Sprint 1 smoke test:** [`docs/sprint1_smoke_checklist.md`](docs/sprint1_smoke_checklist.md) (SCRUM-26).

## License

TBD — internal PoC.
