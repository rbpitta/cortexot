"""PUMP-01 baseline telemetry and scenario overlays."""

import math
import random
from dataclasses import dataclass

from simulator.degradation_scenarios import (
    DegradationState,
    ScenarioName,
    apply_bearing_degradation,
)
from simulator.plant_tags import EQUIPMENT_ID, OPERATING_STATE_TAG


@dataclass
class PumpSample:
    equipment_id: str
    values: dict[str, float | str]

    def as_opcua_dict(self) -> dict[str, float | str]:
        return dict(self.values)


class PumpSimulator:
    def __init__(self, degradation: DegradationState) -> None:
        self._degradation = degradation
        self._tick = 0

    def next_sample(self) -> PumpSample:
        self._tick += 1
        t = self._tick * 0.1
        noise = random.uniform(-0.05, 0.05)
        values: dict[str, float | str] = {
            "temperature": 68.0 + 4.0 * math.sin(t / 30) + noise * 2,
            "pressure": 7.0 + 0.3 * math.sin(t / 20) + noise * 0.1,
            "vibration": 3.0 + 0.5 * math.sin(t / 15) + noise * 0.2,
            "current": 17.0 + 1.0 * math.sin(t / 25) + noise * 0.3,
            "rpm": 1750.0 + 10 * math.sin(t / 40),
            OPERATING_STATE_TAG.name: "running",
        }
        if (
            self._degradation.active
            and self._degradation.scenario == ScenarioName.BEARING_DEGRADATION
        ):
            values = apply_bearing_degradation(
                values, self._degradation.elapsed_minutes()
            )
        return PumpSample(equipment_id=EQUIPMENT_ID, values=values)
