import psycopg
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.config import Settings

router = APIRouter(tags=["health"])


@router.get("/health")
def liveness(request: Request) -> dict:
    settings: Settings = request.app.state.settings
    return {
        "status": "ok",
        "service": settings.service_name,
        "product": "CortexOT",
        "description": settings.app_name,
    }


@router.get("/ready")
def readiness(request: Request) -> JSONResponse:
    settings: Settings = request.app.state.settings
    try:
        with psycopg.connect(
            settings.database_url,
            connect_timeout=settings.database_connect_timeout_seconds,
        ) as conn:
            conn.execute("SELECT 1")
    except Exception as exc:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "service": settings.service_name,
                "database": "unavailable",
                "detail": str(exc),
            },
        )

    return JSONResponse(
        content={
            "status": "ready",
            "service": settings.service_name,
            "database": "ok",
        },
    )
