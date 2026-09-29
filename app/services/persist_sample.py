from datetime import datetime

from app.domain.alarms import evaluate_threshold_alarms
from app.domain.ports import TelemetryPersistencePort
from app.domain.samples import PlantSampleInput


class PersistPlantSample:
    """Save one plant tag reading and derived alarms."""

    def __init__(self, persistence: TelemetryPersistencePort) -> None:
        self._persistence = persistence

    async def execute(
        self,
        time: datetime,
        equipment_id: str,
        tag_name: str,
        raw_value: float | str,
        unit: str,
    ) -> None:
        sample = PlantSampleInput(
            time=time,
            equipment_id=equipment_id,
            tag_name=tag_name,
            raw_value=raw_value,
            unit=unit,
        )
        alarms = []
        if isinstance(raw_value, (int, float)):
            alarms = evaluate_threshold_alarms(equipment_id, tag_name, float(raw_value))
        self._persistence.save_sample(sample, alarms)
