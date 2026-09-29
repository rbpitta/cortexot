import httpx

from app.domain.ports.demo import SimulatorDemoGateway


class HttpxSimulatorDemoGateway(SimulatorDemoGateway):
    def __init__(self, simulator_base_url: str) -> None:
        self._base_url = simulator_base_url.rstrip("/")

    async def start_degradation(self, scenario: str) -> dict:
        url = f"{self._base_url}/api/v1/demo/degradation/start"
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json={"scenario": scenario})
        response.raise_for_status()
        return response.json()
