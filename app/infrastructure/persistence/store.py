import logging
from datetime import UTC, datetime

from sqlalchemy.dialects.postgresql import insert

from app.domain.alarming.evaluate import AlarmDraft
from app.domain.telemetry.sample import PlantSampleInput
from app.infrastructure.persistence.session import get_session_factory
from app.infrastructure.persistence.tables import Alarm, EquipmentState, Measurement

logger = logging.getLogger(__name__)


class SqlAlchemyTelemetryPersistence:
    def save_sample(self, sample: PlantSampleInput, alarms: list[AlarmDraft]) -> None:
        session_factory = get_session_factory()
        raw = sample.raw_value
        with session_factory() as session:
            value: float | None = None
            value_text: str | None = None
            if isinstance(raw, (int, float)):
                value = float(raw)
            else:
                value_text = str(raw)
                if sample.tag_name == "operating_state":
                    ts = sample.time or datetime.now(UTC)
                    stmt = insert(EquipmentState).values(
                        equipment_id=sample.equipment_id,
                        operating_state=value_text,
                        updated_at=ts,
                    )
                    stmt = stmt.on_conflict_do_update(
                        index_elements=["equipment_id"],
                        set_={
                            "operating_state": stmt.excluded.operating_state,
                            "updated_at": stmt.excluded.updated_at,
                        },
                    )
                    session.execute(stmt)

            for alarm in alarms:
                session.add(
                    Alarm(
                        time=sample.time,
                        equipment_id=alarm.equipment_id,
                        tag_name=alarm.tag_name,
                        severity=alarm.severity,
                        message=alarm.message,
                        active=True,
                    )
                )

            session.add(
                Measurement(
                    time=sample.time,
                    equipment_id=sample.equipment_id,
                    tag_name=sample.tag_name,
                    value=value,
                    value_text=value_text,
                    unit=sample.unit or None,
                    source=sample.source,
                )
            )
            try:
                session.commit()
            except Exception:
                session.rollback()
                logger.exception(
                    "Failed to persist measurement %s/%s",
                    sample.equipment_id,
                    sample.tag_name,
                )
