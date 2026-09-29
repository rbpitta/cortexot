from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class SimulatorDemoGateway(Protocol):
    async def start_degradation(self, scenario: str) -> dict[str, Any]: ...
