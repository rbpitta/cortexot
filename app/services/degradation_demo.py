from app.domain.ports import SimulatorDemoGateway


class StartDegradationDemo:
    def __init__(self, gateway: SimulatorDemoGateway) -> None:
        self._gateway = gateway

    async def execute(self, scenario: str) -> dict:
        return await self._gateway.start_degradation(scenario)
