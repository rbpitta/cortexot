"""Run HTTP health/API and OPC-UA plant server together."""

import asyncio
import logging
import os
import threading

import uvicorn

from simulator.degradation_scenarios import DegradationState
from simulator.opcua_server import OpcUaPlantServer
from simulator.pump_simulator import PumpSimulator
from simulator.simulator_app import create_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)

OPCUA_ENDPOINT = os.getenv(
    "OPCUA_ENDPOINT", "opc.tcp://0.0.0.0:4840/cortexot/simulator/"
)
HTTP_HOST = os.getenv("SIMULATOR_HTTP_HOST", "0.0.0.0")
HTTP_PORT = int(os.getenv("SIMULATOR_HTTP_PORT", "8080"))


async def run_opcua(degradation: DegradationState) -> None:
    pump = PumpSimulator(degradation)
    plant_server = OpcUaPlantServer(pump, OPCUA_ENDPOINT)
    await plant_server.start()
    try:
        await asyncio.Event().wait()
    finally:
        await plant_server.stop()


def _run_opcua_thread(degradation: DegradationState) -> None:
    asyncio.run(run_opcua(degradation))


def main() -> None:
    degradation = DegradationState()
    thread = threading.Thread(
        target=_run_opcua_thread,
        args=(degradation,),
        daemon=True,
        name="opcua-server",
    )
    thread.start()
    app = create_app(degradation)
    logger.info("HTTP simulator on %s:%s", HTTP_HOST, HTTP_PORT)
    uvicorn.run(app, host=HTTP_HOST, port=HTTP_PORT, log_level="info")


if __name__ == "__main__":
    main()
