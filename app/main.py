import logging

from fastapi import FastAPI

from app.api.health import router as health_router
from app.config import Settings, get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Headless Industrial AI Advisor — Phase 0 bootstrap",
    )
    app.state.settings = settings
    app.include_router(health_router)
    return app


app = create_app()


@app.on_event("startup")
def on_startup() -> None:
    settings = app.state.settings
    logger.info(
        "Starting %s (%s) env=%s",
        settings.app_name,
        settings.service_name,
        settings.environment,
    )
