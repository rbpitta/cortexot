"""Canonical PUMP-01 process tags (OPC-UA /Plant namespace)."""

from dataclasses import dataclass

EQUIPMENT_ID = "PUMP-01"
NAMESPACE_URI = "http://cortexot.local/plant"


@dataclass(frozen=True)
class PlantTag:
    name: str
    unit: str
    opc_name: str


PLANT_TAGS: tuple[PlantTag, ...] = (
    PlantTag("temperature", "°C", "Temperature"),
    PlantTag("pressure", "bar", "Pressure"),
    PlantTag("vibration", "mm/s", "Vibration"),
    PlantTag("current", "A", "Current"),
    PlantTag("rpm", "rpm", "RPM"),
)

OPERATING_STATE_TAG = PlantTag("operating_state", "", "OperatingState")

TAG_BY_NAME = {t.name: t for t in PLANT_TAGS}
TAG_BY_OPC = {t.opc_name: t for t in PLANT_TAGS}

THRESHOLDS = {
    "temperature": {"warning": 85.0, "critical": 95.0},
    "vibration": {"warning": 6.0, "critical": 8.0},
    "pressure": {"low": 5.0, "high": 9.0},
}
