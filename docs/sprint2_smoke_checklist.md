# Sprint 2 — Phase 1 OPC-UA smoke checklist

Use after `docker compose up --build -d` on branch `develop`.

## 1. Services

| Check | Command / URL | Expected |
|-------|----------------|----------|
| Backend liveness | `GET http://localhost:8000/health` | `status: ok` |
| Backend ready | `GET http://localhost:8000/ready` | `database: ok` |
| Simulator | `GET http://localhost:8080/health` | `opcua: configured` |
| MCP placeholder | `GET http://localhost:8001/health` | `status: ok` |

## 2. OPC-UA (optional UaExpert)

- Endpoint: `opc.tcp://localhost:4840/cortexot/simulator/`
- Browse: `Objects → Plant → PUMP-01` (Temperature, Pressure, Vibration, Current, RPM, OperatingState)

## 3. Degradation demo

```bash
curl -X POST http://localhost:8000/api/v1/demo/degradation/start \
  -H "Content-Type: application/json" \
  -d "{\"scenario\":\"bearing_degradation\"}"
```

## 4. TimescaleDB

Connect pgAdmin to `localhost:5432` (user/db/password `cortexot`).

```sql
SELECT time, tag_name, value
FROM cortexot.measurements
WHERE equipment_id = 'PUMP-01'
ORDER BY time DESC
LIMIT 20;
```

After ~1–2 minutes you should see rows with `source = opcua`.

## 5. Automated tests (local)

```bash
pip install -e ".[dev]"
python -m pytest
```

Optional integration (stack + DB running):

```bash
set RUN_OPCUA_INTEGRATION=1
python -m pytest -m integration
```

## Jira

Paste evidence into **SCRUM-36** when closing Phase 1 integration validation.
