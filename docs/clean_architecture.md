# Clean Architecture & SOLID (CortexOT)

CortexOT is a **modular monolith**: one repository, multiple deployable services (`cortexot-backend`, `cortexot-simulator`, …). The backend follows **Clean Architecture** with explicit layers and dependency rules.

## Layers (backend)

| Layer | Package | Responsibility |
|-------|---------|----------------|
| **Domain** | `app.domain` | Business rules, entities, pure functions. No FastAPI, SQLAlchemy, asyncua, or simulator imports. |
| **Application** | `app.application` | Use cases orchestrating domain + ports. |
| **Infrastructure** | `app.infrastructure` | Adapters: DB, OPC-UA, HTTP clients. |
| **Presentation** | `app.presentation` | HTTP routes, background workers (thin). |
| **Composition** | `app.bootstrap` | Wires implementations to ports (single place). |

Shared plant contract (tags, thresholds, namespace URI): **`cortexot_plant`** — used by backend and simulator, not `app → simulator`.

## Dependency rule

```text
presentation → application → domain
infrastructure → domain (implements ports)
```

- `app.domain` must **not** import `app.infrastructure`, `app.presentation`, `simulator`, or framework libraries.
- `app.application` imports only `app.domain` and port protocols.
- Cross-cutting config: `app.config` (settings only).

## SOLID (practical PoC rules)

- **SRP:** One module, one reason to change (alarm evaluation ≠ OPC-UA subscription ≠ SQL persistence).
- **OCP:** Extend scenarios via strategies/registries, not scattered conditionals in workers.
- **LSP:** Port implementations are swappable (fakes in unit tests).
- **ISP:** Small ports (`PlantTelemetryPort`, `TelemetryPersistencePort`, `SimulatorDemoGateway`).
- **DIP:** Workers and use cases depend on ports; `bootstrap.py` injects concrete adapters.

## Clean Code

- Prefer readable names over clever abstractions.
- Keep functions short; avoid deep nesting.
- Comments only for non-obvious business rules (e.g. degradation timelines).

## Static analysis

- **Snyk Code** (SAST): security and quality — see [development.md](development.md).
- Optional: **import-linter** enforces layer boundaries in CI.

## Related

- [architecture.md](architecture.md) — product/system view
- [repository_layout.md](repository_layout.md) — all top-level folders (`agent/`, `analytics/`, `simulator/`, …)
- [development.md](development.md) — local dev, tests, Snyk
