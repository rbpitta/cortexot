from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.base import Base


class Equipment(Base):
    __tablename__ = "equipment"
    __table_args__ = {"schema": "cortexot"}

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    equipment_type: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Measurement(Base):
    __tablename__ = "measurements"
    __table_args__ = {"schema": "cortexot"}

    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    equipment_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tag_name: Mapped[str] = mapped_column(String(64), primary_key=True)
    value: Mapped[float | None] = mapped_column(Float, nullable=True)
    value_text: Mapped[str | None] = mapped_column(String(64), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(32), nullable=True)
    source: Mapped[str] = mapped_column(String(32), nullable=False, default="opcua")


class EquipmentState(Base):
    __tablename__ = "equipment_state"
    __table_args__ = {"schema": "cortexot"}

    equipment_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    operating_state: Mapped[str] = mapped_column(String(32), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Alarm(Base):
    __tablename__ = "alarms"
    __table_args__ = {"schema": "cortexot"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    equipment_id: Mapped[str] = mapped_column(String(64), nullable=False)
    tag_name: Mapped[str] = mapped_column(String(64), nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    cleared_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
