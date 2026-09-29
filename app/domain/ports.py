from typing import Any, Protocol, runtime_checkable

from app.domain.alarms import AlarmDraft
from app.domain.samples import PlantSampleInput


@runtime_checkable
class TelemetryPersistencePort(Protocol):
    def save_sample(self, sample: PlantSampleInput, alarms: list[AlarmDraft]) -> None: ...


@runtime_checkable
class PlantTelemetryPort(Protocol):
    async def start(self, period_ms: int) -> None: ...

    async def stop(self) -> None: ...


@runtime_checkable
class SimulatorDemoGateway(Protocol):
    async def start_degradation(self, scenario: str) -> dict[str, Any]: ...
