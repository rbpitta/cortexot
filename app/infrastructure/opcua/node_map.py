"""Browse paths and logical tag names for /Plant/PUMP-01."""

from dataclasses import dataclass

from cortexot_plant.plant_tags import (
    EQUIPMENT_ID,
    NAMESPACE_URI,
    OPERATING_STATE_TAG,
    PLANT_TAGS,
)


@dataclass(frozen=True)
class MappedTag:
    equipment_id: str
    tag_name: str
    unit: str
    opc_name: str


def plant_tags_for_equipment() -> list[MappedTag]:
    tags: list[MappedTag] = []
    for tag in PLANT_TAGS:
        tags.append(
            MappedTag(
                equipment_id=EQUIPMENT_ID,
                tag_name=tag.name,
                unit=tag.unit,
                opc_name=tag.opc_name,
            )
        )
    tags.append(
        MappedTag(
            equipment_id=EQUIPMENT_ID,
            tag_name=OPERATING_STATE_TAG.name,
            unit=OPERATING_STATE_TAG.unit,
            opc_name=OPERATING_STATE_TAG.opc_name,
        )
    )
    return tags


def resolve_namespace_index(server_namespaces: list[str]) -> int:
    try:
        return server_namespaces.index(NAMESPACE_URI)
    except ValueError as exc:
        raise RuntimeError(f"namespace {NAMESPACE_URI!r} not found on server") from exc
