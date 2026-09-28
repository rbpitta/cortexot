"""Phase 0 placeholder for cortexot-mcp (Industrial MCP server)."""

import logging

from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVICE_NAME = "cortexot-mcp"
PRODUCT = "CortexOT"
LAYER = "Industrial MCP"

app = FastAPI(
    title="Industrial MCP",
    description="CortexOT Industrial MCP — Phase 0 placeholder (tools in later phases)",
    version="0.1.0",
)


@app.on_event("startup")
def on_startup() -> None:
    logger.info("Starting %s (%s)", LAYER, SERVICE_NAME)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "product": PRODUCT,
        "layer": LAYER,
        "phase": "0-placeholder",
    }
