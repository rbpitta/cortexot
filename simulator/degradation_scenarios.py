"""Progressive abnormal operating scenarios for demo."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum


class ScenarioName(str, Enum):
    BEARING_DEGRADATION = "bearing_degradation"


@dataclass
class DegradationState:
    active: bool = False
    scenario: ScenarioName | None = None
    started_at: datetime | None = field(default=None, compare=False)

    def start(self, scenario: ScenarioName) -> None:
        self.active = True
        self.scenario = scenario
        self.started_at = datetime.now(UTC)

    def stop(self) -> None:
        self.active = False
        self.scenario = None
        self.started_at = None

    def elapsed_minutes(self) -> float:
        if not self.active or self.started_at is None:
            return 0.0
        return (datetime.now(UTC) - self.started_at).total_seconds() / 60.0


def apply_bearing_degradation(
    base: dict[str, float | str],
    elapsed_min: float,
) -> dict[str, float | str]:
    """Vibration ramp first, then temperature lag (PoC timeline)."""
    out = dict(base)
    if elapsed_min < 5:
        return out
    ramp_min = max(0.0, elapsed_min - 5)
    out["vibration"] = float(out["vibration"]) + ramp_min * 0.15
    if elapsed_min >= 15:
        temp_ramp = max(0.0, elapsed_min - 15)
        out["temperature"] = float(out["temperature"]) + temp_ramp * 0.3
    if elapsed_min >= 5:
        out["current"] = float(out["current"]) + min(ramp_min * 0.05, 2.0)
    return out
