"""Phase 0 placeholder for cortexot-simulator (OPC-UA in Phase 1+)."""

import logging

from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVICE_NAME = "cortexot-simulator"
PRODUCT = "CortexOT"

app = FastAPI(
    title="CortexOT Simulator",
    description="Industrial process simulator — Phase 0 placeholder (OPC-UA in Phase 1)",
    version="0.1.0",
)


@app.on_event("startup")
def on_startup() -> None:
    logger.info("Starting %s", SERVICE_NAME)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "product": PRODUCT,
        "phase": "0-placeholder",
        "opcua": "not_configured",
    }
