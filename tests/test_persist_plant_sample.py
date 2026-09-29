from datetime import UTC, datetime

import pytest

from app.application.use_cases.persist_plant_sample import PersistPlantSample
from app.domain.alarming.evaluate import AlarmDraft
from app.domain.telemetry.sample import PlantSampleInput


class FakePersistence:
    def __init__(self) -> None:
        self.samples: list[PlantSampleInput] = []
        self.alarms: list[AlarmDraft] = []

    def save_sample(self, sample: PlantSampleInput, alarms: list[AlarmDraft]) -> None:
        self.samples.append(sample)
        self.alarms.extend(alarms)


@pytest.mark.asyncio
async def test_persist_plant_sample_triggers_alarm_evaluation() -> None:
    fake = FakePersistence()
    use_case = PersistPlantSample(fake)
    ts = datetime.now(UTC)
    await use_case.execute(ts, "PUMP-01", "vibration", 9.0, "mm/s")
    assert len(fake.samples) == 1
    assert fake.samples[0].tag_name == "vibration"
    assert len(fake.alarms) == 1
    assert fake.alarms[0].severity == "critical"
