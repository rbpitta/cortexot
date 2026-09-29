"""Run Alembic upgrade on startup when enabled."""

import logging
import os
from pathlib import Path

from alembic import command
from alembic.config import Config

logger = logging.getLogger(__name__)


def run_migrations() -> None:
    if os.getenv("RUN_DB_MIGRATIONS", "true").lower() not in ("1", "true", "yes"):
        logger.info("Skipping DB migrations (RUN_DB_MIGRATIONS=false)")
        return
    root = Path(__file__).resolve().parents[1]
    cfg = Config(str(root / "alembic.ini"))
    cfg.set_main_option("script_location", str(root / "alembic"))
    logger.info("Running Alembic upgrade head")
    command.upgrade(cfg, "head")
