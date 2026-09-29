"""Background OPC-UA subscription collector."""

import asyncio
import logging

from app.config import Settings
from app.domain.ports.telemetry import PlantTelemetryPort

logger = logging.getLogger(__name__)


class OpcUaCollectorWorker:
    def __init__(self, settings: Settings, telemetry: PlantTelemetryPort) -> None:
        self._settings = settings
        self._telemetry = telemetry
        self._task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        if not self._settings.opcua_enabled:
            logger.info("OPC-UA collector disabled (OPCUA_ENABLED=false)")
            return

        async def _run_with_retry() -> None:
            delay = 2.0
            while True:
                try:
                    await self._telemetry.start(
                        period_ms=self._settings.opcua_subscription_period_ms
                    )
                    while True:
                        await asyncio.sleep(3600)
                except asyncio.CancelledError:
                    raise
                except Exception:
                    logger.exception(
                        "OPC-UA collector error; retry in %.0fs", delay
                    )
                    await self._telemetry.stop()
                    await asyncio.sleep(delay)
                    delay = min(delay * 2, 60.0)

        self._task = asyncio.create_task(_run_with_retry())
        logger.info(
            "OPC-UA collector started for %s", self._settings.opcua_endpoint
        )

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
        await self._telemetry.stop()
