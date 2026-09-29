from dataclasses import dataclass

from cortexot_plant.plant_tags import THRESHOLDS


@dataclass(frozen=True)
class AlarmDraft:
    equipment_id: str
    tag_name: str
    severity: str
    message: str


def evaluate_threshold_alarms(
    equipment_id: str,
    tag_name: str,
    value: float,
) -> list[AlarmDraft]:
    rules = THRESHOLDS.get(tag_name)
    if not rules:
        return []

    severity: str | None = None
    message: str | None = None
    if "critical" in rules and value >= rules["critical"]:
        severity = "critical"
        message = f"{tag_name} critical: {value:.2f}"
    elif "warning" in rules and value >= rules["warning"]:
        severity = "warning"
        message = f"{tag_name} warning: {value:.2f}"
    elif "high" in rules and value >= rules["high"]:
        severity = "warning"
        message = f"{tag_name} high: {value:.2f}"
    elif "low" in rules and value <= rules["low"]:
        severity = "warning"
        message = f"{tag_name} low: {value:.2f}"

    if not severity or not message:
        return []
    return [
        AlarmDraft(
            equipment_id=equipment_id,
            tag_name=tag_name,
            severity=severity,
            message=message,
        )
    ]
