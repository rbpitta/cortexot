from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from mcp.placeholder_app import app as mcp_app
from simulator.placeholder_app import app as simulator_app


def test_backend_liveness(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "cortexot-backend"
    assert body["product"] == "CortexOT"


def test_backend_readiness_without_database(monkeypatch) -> None:
    settings = Settings(
        database_url="postgresql://invalid:invalid@127.0.0.1:1/nodb",
        opcua_enabled=False,
        run_db_migrations=False,
    )
    app = create_app(settings=settings)
    client = TestClient(app)

    response = client.get("/ready")
    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "not_ready"
    assert body["database"] == "unavailable"


def test_mcp_placeholder_health() -> None:
    client = TestClient(mcp_app)
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "cortexot-mcp"
    assert body["layer"] == "Industrial MCP"


def test_simulator_placeholder_health() -> None:
    client = TestClient(simulator_app)
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "cortexot-simulator"
    assert body["opcua"] == "configured"
