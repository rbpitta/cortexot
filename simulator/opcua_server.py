"""AsyncUA server exposing /Plant/PUMP-01/* process variables."""

import asyncio
import logging
from typing import Any

from asyncua import Server, ua

from simulator.plant_tags import (
    NAMESPACE_URI,
    OPERATING_STATE_TAG,
    PLANT_TAGS,
)
from simulator.pump_simulator import PumpSimulator

logger = logging.getLogger(__name__)

UPDATE_INTERVAL_SEC = 1.0


class OpcUaPlantServer:
    def __init__(self, pump: PumpSimulator, endpoint: str) -> None:
        self._pump = pump
        self._endpoint = endpoint
        self._server: Server | None = None
        self._variables: dict[str, Any] = {}
        self._task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        server = Server()
        await server.init()
        server.set_endpoint(self._endpoint)
        server.set_server_name("CortexOT Plant Simulator")
        idx = await server.register_namespace(NAMESPACE_URI)
        objects = server.nodes.objects
        plant = await objects.add_object(idx, "Plant")
        pump_node = await plant.add_object(idx, "PUMP-01")

        for tag in PLANT_TAGS:
            initial = 0.0
            var = await pump_node.add_variable(idx, tag.opc_name, initial)
            await var.set_writable()
            self._variables[tag.name] = var

        state_var = await pump_node.add_variable(
            idx, OPERATING_STATE_TAG.opc_name, "running"
        )
        await state_var.set_writable()
        self._variables[OPERATING_STATE_TAG.name] = state_var

        await server.start()
        self._server = server
        self._task = asyncio.create_task(self._telemetry_loop())
        logger.info("OPC-UA server listening on %s", self._endpoint)

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        if self._server:
            await self._server.stop()
            self._server = None

    async def _telemetry_loop(self) -> None:
        while True:
            sample = self._pump.next_sample()
            for name, value in sample.values.items():
                node = self._variables.get(name)
                if node is None:
                    continue
                if isinstance(value, str):
                    await node.write_value(value, varianttype=ua.VariantType.String)
                else:
                    await node.write_value(float(value))
            await asyncio.sleep(UPDATE_INTERVAL_SEC)
