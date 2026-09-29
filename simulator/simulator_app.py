"""HTTP surface for simulator health and demo controls."""

import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from simulator.degradation_scenarios import DegradationState, ScenarioName

logger = logging.getLogger(__name__)

SERVICE_NAME = "cortexot-simulator"
PRODUCT = "CortexOT"


class DegradationStartRequest(BaseModel):
    scenario: str = Field(default="bearing_degradation")


def create_app(degradation: DegradationState | None = None) -> FastAPI:
    state = degradation if degradation is not None else DegradationState()

    app = FastAPI(
        title="CortexOT Simulator",
        description="Industrial process simulator with OPC-UA /Plant",
        version="0.2.0",
    )
    app.state.degradation = state

    @app.on_event("startup")
    def on_startup() -> None:
        logger.info("Starting %s (HTTP)", SERVICE_NAME)

    @app.get("/health")
    def health() -> dict:
        return {
            "status": "ok",
            "service": SERVICE_NAME,
            "product": PRODUCT,
            "phase": "1-opcua",
            "opcua": "configured",
        }

    @app.post("/api/v1/demo/degradation/start")
    def start_degradation(body: DegradationStartRequest) -> dict:
        try:
            scenario = ScenarioName(body.scenario)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="unknown scenario") from exc
        state.start(scenario)
        logger.info("Degradation started: %s", scenario.value)
        return {
            "status": "started",
            "scenario": scenario.value,
            "active": state.active,
        }

    @app.post("/api/v1/demo/degradation/stop")
    def stop_degradation() -> dict:
        state.stop()
        return {"status": "stopped", "active": state.active}

    return app
