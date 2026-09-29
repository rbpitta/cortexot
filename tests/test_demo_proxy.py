from fastapi.testclient import TestClient

from app.application.use_cases.start_degradation_demo import StartDegradationDemo
from app.bootstrap import AppContainer, build_container
from app.config import Settings
from app.main import create_app


class FakeSimulatorGateway:
    def __init__(self) -> None:
        self.last_scenario: str | None = None

    async def start_degradation(self, scenario: str) -> dict:
        self.last_scenario = scenario
        return {"status": "started", "scenario": scenario}


def test_degradation_start_uses_demo_use_case() -> None:
    settings = Settings(
        simulator_base_url="http://sim:8080",
        opcua_enabled=False,
        run_db_migrations=False,
    )
    base = build_container(settings)
    gateway = FakeSimulatorGateway()
    container = AppContainer(
        settings=settings,
        persist_plant_sample=base.persist_plant_sample,
        start_degradation_demo=StartDegradationDemo(gateway),
        plant_telemetry=base.plant_telemetry,
        opcua_collector_worker=base.opcua_collector_worker,
    )
    client = TestClient(create_app(settings=settings, container=container))
    response = client.post(
        "/api/v1/demo/degradation/start",
        json={"scenario": "bearing_degradation"},
    )
    assert response.status_code == 200
    assert gateway.last_scenario == "bearing_degradation"
