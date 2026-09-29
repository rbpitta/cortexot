import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.demo import router as demo_router
from app.api.health import router as health_router
from app.bootstrap import AppContainer, build_container
from app.config import Settings, get_settings
from app.db_migrate import run_migrations

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


def create_app(
    settings: Settings | None = None,
    container: AppContainer | None = None,
) -> FastAPI:
    settings = settings or get_settings()
    container = container or build_container(settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if settings.run_db_migrations:
            run_migrations()
        await container.opcua_collector_worker.start()
        logger.info(
            "Starting %s (%s) env=%s",
            settings.app_name,
            settings.service_name,
            settings.environment,
        )
        yield
        await container.opcua_collector_worker.stop()

    app = FastAPI(
        title=settings.app_name,
        version="0.3.1",
        description="Headless Industrial AI Advisor",
        lifespan=lifespan,
    )
    app.state.settings = settings
    app.state.container = container
    app.include_router(health_router)
    app.include_router(demo_router)
    return app


app = create_app()
