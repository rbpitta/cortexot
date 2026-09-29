from app.application.use_cases.persist_plant_sample import PersistPlantSample
from app.domain.ports.telemetry import PlantTelemetryPort
from app.infrastructure.opcua.plant_subscriber import AsyncUaPlantSubscriber


class AsyncUaPlantTelemetryAdapter(PlantTelemetryPort):
    """OPC-UA adapter: subscriptions invoke the persist use case."""

    def __init__(self, endpoint: str, persist_sample: PersistPlantSample) -> None:
        self._endpoint = endpoint
        self._persist_sample = persist_sample
        self._subscriber: AsyncUaPlantSubscriber | None = None

    async def start(self, period_ms: int = 1000) -> None:
        async def on_sample(ts, equipment_id, tag_name, raw, unit):
            await self._persist_sample.execute(ts, equipment_id, tag_name, raw, unit)

        self._subscriber = AsyncUaPlantSubscriber(self._endpoint, on_sample)
        await self._subscriber.start(period_ms=period_ms)

    async def stop(self) -> None:
        if self._subscriber:
            await self._subscriber.stop()
            self._subscriber = None
