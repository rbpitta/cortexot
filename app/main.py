import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.demo import router as demo_router
from app.api.health import router as health_router
from app.config import Settings, get_settings
from app.db_migrate import run_migrations
from app.workers.opcua_collector_worker import OpcUaCollectorWorker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if settings.run_db_migrations:
            run_migrations()
        collector = OpcUaCollectorWorker(settings)
        app.state.opcua_collector = collector
        await collector.start()
        logger.info(
            "Starting %s (%s) env=%s",
            settings.app_name,
            settings.service_name,
            settings.environment,
        )
        yield
        await collector.stop()

    app = FastAPI(
        title=settings.app_name,
        version="0.2.0",
        description="Headless Industrial AI Advisor — Phase 1 OPC-UA ingest",
        lifespan=lifespan,
    )
    app.state.settings = settings
    app.include_router(health_router)
    app.include_router(demo_router)
    return app


app = create_app()
