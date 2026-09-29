from typing import Protocol, runtime_checkable


@runtime_checkable
class PlantTelemetrySink(Protocol):
    async def on_plant_sample(
        self,
        time,
        equipment_id: str,
        tag_name: str,
        raw_value: float | str,
        unit: str,
    ) -> None: ...


@runtime_checkable
class PlantTelemetryPort(Protocol):
    async def start(self, period_ms: int) -> None: ...

    async def stop(self) -> None: ...
