import httpx
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/demo", tags=["demo"])


class DegradationStartBody(BaseModel):
    scenario: str = Field(default="bearing_degradation")


@router.post("/degradation/start")
async def start_degradation(request: Request, body: DegradationStartBody) -> dict:
    use_case = request.app.state.container.start_degradation_demo
    try:
        return await use_case.execute(body.scenario)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text) from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail="simulator unreachable") from exc
