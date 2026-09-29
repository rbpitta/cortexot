"""Phase 1 plant telemetry tables and hypertable

Revision ID: 001_phase1
Revises:
Create Date: 2026-03-28

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001_phase1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS cortexot")

    op.create_table(
        "equipment",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("equipment_type", sa.String(64), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        schema="cortexot",
    )

    op.create_table(
        "measurements",
        sa.Column("time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("equipment_id", sa.String(64), nullable=False),
        sa.Column("tag_name", sa.String(64), nullable=False),
        sa.Column("value", sa.Float(), nullable=True),
        sa.Column("value_text", sa.String(64), nullable=True),
        sa.Column("unit", sa.String(32), nullable=True),
        sa.Column("source", sa.String(32), nullable=False, server_default="opcua"),
        sa.PrimaryKeyConstraint("time", "equipment_id", "tag_name"),
        schema="cortexot",
    )
    op.execute(
        "SELECT create_hypertable('cortexot.measurements', 'time', if_not_exists => TRUE)"
    )

    op.create_table(
        "equipment_state",
        sa.Column("equipment_id", sa.String(64), primary_key=True),
        sa.Column("operating_state", sa.String(32), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        schema="cortexot",
    )

    op.create_table(
        "alarms",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "time",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("equipment_id", sa.String(64), nullable=False),
        sa.Column("tag_name", sa.String(64), nullable=False),
        sa.Column("severity", sa.String(16), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("cleared_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="cortexot",
    )

    op.execute(
        """
        INSERT INTO cortexot.equipment (id, name, equipment_type)
        VALUES ('PUMP-01', 'Primary process pump', 'centrifugal_pump')
        ON CONFLICT (id) DO NOTHING
        """
    )


def downgrade() -> None:
    op.drop_table("alarms", schema="cortexot")
    op.drop_table("equipment_state", schema="cortexot")
    op.drop_table("measurements", schema="cortexot")
    op.drop_table("equipment", schema="cortexot")
