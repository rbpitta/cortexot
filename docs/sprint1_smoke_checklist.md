# Sprint 1 — Phase 0 smoke checklist (SCRUM-26)

Run from the repository root with Docker Desktop available.

## 1. Validate Compose file

```bash
docker compose config
```

Expected: exit code 0, five services defined (no MQTT profile).

## 2. Start stack

```bash
cp .env.example .env
docker compose up --build -d
```

Wait until all containers are healthy (first Ollama start may take longer).

## 3. Health checks

| Service | Check |
|---------|--------|
| cortexot-backend | `curl -sf http://localhost:8000/health` and `curl -sf http://localhost:8000/ready` |
| cortexot-mcp | `curl -sf http://localhost:8001/health` |
| cortexot-simulator | `curl -sf http://localhost:8080/health` |
| cortexot-timescaledb | `docker exec cortexot-timescaledb pg_isready -U cortexot` |
| cortexot-ollama | `curl -sf http://localhost:11434/` |

## 4. Timescale extension

```bash
docker exec cortexot-timescaledb psql -U cortexot -d cortexot -c "SELECT extname FROM pg_extension WHERE extname = 'timescaledb';"
```

Expected: one row `timescaledb`.

## 5. Unit tests (host Python)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
pytest -q
```

Expected: all tests pass.

## 6. Teardown (optional)

```bash
docker compose down
```

Paste command outputs into Jira **SCRUM-26** when closing the issue.
