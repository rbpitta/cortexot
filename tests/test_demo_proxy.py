import httpx
import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def test_degradation_start_proxies_to_simulator(monkeypatch) -> None:
    captured: dict = {}

    async def mock_post(url: str, json: dict) -> httpx.Response:
        captured["url"] = url
        captured["json"] = json
        return httpx.Response(200, json={"status": "started", "scenario": json["scenario"]})

    class MockAsyncClient:
        def __init__(self, *args, **kwargs) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def post(self, url: str, json: dict) -> httpx.Response:
            return await mock_post(url, json)

    monkeypatch.setattr("app.api.demo.httpx.AsyncClient", MockAsyncClient)

    settings = Settings(
        simulator_base_url="http://sim:8080",
        opcua_enabled=False,
        run_db_migrations=False,
    )
    client = TestClient(create_app(settings=settings))
    response = client.post(
        "/api/v1/demo/degradation/start",
        json={"scenario": "bearing_degradation"},
    )
    assert response.status_code == 200
    assert captured["url"] == "http://sim:8080/api/v1/demo/degradation/start"
