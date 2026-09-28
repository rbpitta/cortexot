# CortexOT — Industrial AI Advisor

Headless Industrial AI platform integrated with SCADA/supervisory systems via **OPC-UA** (primary). This repository is a Proof of Concept evolving toward a production-grade advisor: collect process data, detect anomalies, investigate with a local LLM (Ollama) and **Industrial MCP** tools, and publish structured recommendations back to SCADA for operator acceptance.

**Phase 0** provides the Docker stack, FastAPI bootstrap, health checks, and placeholders only — no OPC-UA, agent, or MCP tools yet.

## Stack (Phase 0)

| Service | Container name | Role |
|---------|----------------|------|
| Backend | `cortexot-backend` | FastAPI API, future collectors & agent |
| Industrial MCP | `cortexot-mcp` | MCP tool layer (placeholder) |
| Simulator | `cortexot-simulator` | Industrial simulator (placeholder) |
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
- Simulator: http://localhost:8080/health
- Ollama: http://localhost:11434/

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

## License

TBD — internal PoC.
