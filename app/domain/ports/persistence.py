from typing import Protocol, runtime_checkable

from app.domain.alarming.evaluate import AlarmDraft
from app.domain.telemetry.sample import PlantSampleInput


@runtime_checkable
class TelemetryPersistencePort(Protocol):
    def save_sample(self, sample: PlantSampleInput, alarms: list[AlarmDraft]) -> None: ...
