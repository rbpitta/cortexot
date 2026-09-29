"""Persist OPC-UA samples and evaluate simple thresholds."""

import logging
from datetime import UTC, datetime

from sqlalchemy.dialects.postgresql import insert

from models.db.session import get_session_factory
from models.db.tables import Alarm, EquipmentState, Measurement
from simulator.plant_tags import THRESHOLDS

logger = logging.getLogger(__name__)


def _evaluate_alarms(
    session,
    equipment_id: str,
    tag_name: str,
    value: float,
    ts: datetime,
) -> None:
    rules = THRESHOLDS.get(tag_name)
    if not rules:
        return
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
    if severity and message:
        session.add(
            Alarm(
                time=ts,
                equipment_id=equipment_id,
                tag_name=tag_name,
                severity=severity,
                message=message,
                active=True,
            )
        )


async def persist_sample(
    ts: datetime,
    equipment_id: str,
    tag_name: str,
    raw: float | str,
    unit: str,
) -> None:
    session_factory = get_session_factory()
    with session_factory() as session:
        if isinstance(raw, (int, float)):
            value = float(raw)
            value_text = None
            _evaluate_alarms(session, equipment_id, tag_name, value, ts)
        else:
            value = None
            value_text = str(raw)
            if tag_name == "operating_state":
                stmt = insert(EquipmentState).values(
                    equipment_id=equipment_id,
                    operating_state=value_text,
                    updated_at=ts or datetime.now(UTC),
                )
                stmt = stmt.on_conflict_do_update(
                    index_elements=["equipment_id"],
                    set_={
                        "operating_state": stmt.excluded.operating_state,
                        "updated_at": stmt.excluded.updated_at,
                    },
                )
                session.execute(stmt)
        session.add(
            Measurement(
                time=ts,
                equipment_id=equipment_id,
                tag_name=tag_name,
                value=value,
                value_text=value_text,
                unit=unit or None,
                source="opcua",
            )
        )
        try:
            session.commit()
        except Exception:
            session.rollback()
            logger.exception("Failed to persist measurement %s/%s", equipment_id, tag_name)
