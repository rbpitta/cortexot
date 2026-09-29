# Development guide

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

Architecture conventions: [clean_architecture.md](clean_architecture.md).

## Tests

```bash
python -m pytest
```

Integration (Docker stack running):

```bash
set RUN_OPCUA_INTEGRATION=1
python -m pytest -m integration
```

## Layer boundaries (import-linter)

```bash
python -m importlinter.cli lint-imports
```

Fails if `app.domain` or `app.application` import infrastructure, presentation, or frameworks.

## Snyk Code (static analysis)

Snyk Code scans for security issues and unsafe patterns in Python source.

### Local

1. Install [Snyk CLI](https://docs.snyk.io/developer-tools/snyk-cli/install-the-snyk-cli).
2. `snyk auth` (once per machine).
3. From repo root: `snyk code test`

Optional stricter gate:

```bash
snyk code test --severity-threshold=high
```

### CI

GitHub Actions workflow [`.github/workflows/snyk-code.yml`](../.github/workflows/snyk-code.yml) runs on push/PR to `develop` and `main`.

Add repository secret **`SNYK_TOKEN`** (Snyk account → Organization → Service accounts / API token).

### PoC policy

- **High / Critical:** fix before merge (or documented exception in Jira).
- **Medium / Low:** triage; baseline may be relaxed during first sprint after adoption.

Do not commit `.env` or tokens. Snyk does not replace readable-code review or optional formatters (e.g. Ruff) later.
