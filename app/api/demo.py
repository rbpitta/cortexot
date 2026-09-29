import httpx
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/demo", tags=["demo"])


class DegradationStartBody(BaseModel):
    scenario: str = Field(default="bearing_degradation")


@router.post("/degradation/start")
async def start_degradation(request: Request, body: DegradationStartBody) -> dict:
    settings = request.app.state.settings
    url = f"{settings.simulator_base_url.rstrip('/')}/api/v1/demo/degradation/start"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=body.model_dump())
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail="simulator unreachable") from exc
    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()
