# Code organization (CortexOT backend)

We keep **SOLID** and **dependency direction** without deep folder trees.

## Why not `application/use_cases/`?

“Use case” is a DDD/Clean Architecture term for **one user-facing action** (e.g. save a plant sample). The idea is valid; nested folders (`application` → `use_cases` → file) added ceremony without clarity for a small PoC.

We use **`app/services/`** instead: short modules that orchestrate **domain** rules and **ports** (interfaces). Same responsibility, fewer clicks.

## Layout

```text
app/
  domain/          # Pure rules: alarms.py, samples.py, ports.py
  services/        # Orchestration (persist sample, start degradation demo)
  db/              # SQLAlchemy + Timescale persistence
  opcua/           # OPC-UA client/subscriber adapters
  api/             # FastAPI routes (thin)
  workers/         # Background collector (thin)
  bootstrap.py     # Wire dependencies (composition root)
  main.py          # App factory
cortexot_plant/    # Shared tag/threshold contract (backend + simulator)
simulator/         # Separate deployable
mcp/               # Separate deployable
```

**Rule:** `domain` and `services` do not import `db`, `opcua`, FastAPI, or SQLAlchemy. Adapters implement `domain.ports`; `bootstrap.py` connects them.

## SOLID (short)

- **SRP:** alarms ≠ DB ≠ OPC-UA subscription.
- **DIP:** services depend on `TelemetryPersistencePort`, not SQL directly.
- **Tests:** fake persistence in unit tests; no OPC-UA required.

## Quality gates

- [development.md](development.md) — pytest, import-linter, Snyk Code
- [repository_layout.md](repository_layout.md) — whole repo

Future phases (analytics, agent) add **new folders only when code lands**, not empty placeholders.
