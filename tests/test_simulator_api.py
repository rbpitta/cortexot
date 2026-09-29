from fastapi.testclient import TestClient

from simulator.simulator_app import create_app


def test_start_bearing_degradation() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/demo/degradation/start",
        json={"scenario": "bearing_degradation"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "started"
    assert body["scenario"] == "bearing_degradation"
