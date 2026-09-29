"""OPC-UA → Timescale integration (requires running stack)."""

import asyncio
import os
import time

import psycopg
import pytest

OPCUA_ENDPOINT = os.getenv(
    "OPCUA_ENDPOINT", "opc.tcp://localhost:4840/cortexot/simulator/"
)
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://cortexot:cortexot@localhost:5432/cortexot"
)


def _integration_enabled() -> bool:
    return os.getenv("RUN_OPCUA_INTEGRATION", "").lower() in ("1", "true", "yes")


pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def require_integration():
    if not _integration_enabled():
        pytest.skip("Set RUN_OPCUA_INTEGRATION=1 with Docker stack up")


@pytest.mark.asyncio
async def test_opcua_subscription_persists_measurement(require_integration) -> None:
    from integrations.opcua.plant_subscriber import PlantSubscriber

    received: list[tuple[str, float | str]] = []

    async def on_sample(ts, equipment_id, tag_name, raw, unit):
        received.append((tag_name, raw))

    sub = PlantSubscriber(OPCUA_ENDPOINT, on_sample)
    await sub.start(period_ms=1000)
    try:
        deadline = time.time() + 30
        while time.time() < deadline and not received:
            await asyncio.sleep(0.5)
        assert received, "no OPC-UA samples within 30s"
    finally:
        await sub.stop()

    deadline = time.time() + 30
    row = None
    while time.time() < deadline:
        with psycopg.connect(DATABASE_URL, connect_timeout=3) as conn:
            row = conn.execute(
                """
                SELECT equipment_id, tag_name, source
                FROM cortexot.measurements
                WHERE equipment_id = 'PUMP-01'
                ORDER BY time DESC
                LIMIT 1
                """
            ).fetchone()
        if row:
            break
        time.sleep(2)

    assert row is not None, "no rows in cortexot.measurements (is backend collector running?)"
    assert row[0] == "PUMP-01"
    assert row[2] == "opcua"
