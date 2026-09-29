from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PlantSampleInput:
    time: datetime
    equipment_id: str
    tag_name: str
    raw_value: float | str
    unit: str
    source: str = "opcua"
