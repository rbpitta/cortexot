from dataclasses import dataclass

from app.application.use_cases.persist_plant_sample import PersistPlantSample
from app.application.use_cases.start_degradation_demo import StartDegradationDemo
from app.config import Settings
from app.domain.ports.telemetry import PlantTelemetryPort
from app.infrastructure.http.simulator_gateway import HttpxSimulatorDemoGateway
from app.infrastructure.opcua.telemetry_adapter import AsyncUaPlantTelemetryAdapter
from app.infrastructure.persistence.store import SqlAlchemyTelemetryPersistence
from app.presentation.workers.opcua_collector_worker import OpcUaCollectorWorker


@dataclass
class AppContainer:
    settings: Settings
    persist_plant_sample: PersistPlantSample
    start_degradation_demo: StartDegradationDemo
    plant_telemetry: PlantTelemetryPort
    opcua_collector_worker: OpcUaCollectorWorker


def build_container(settings: Settings) -> AppContainer:
    persistence = SqlAlchemyTelemetryPersistence()
    persist_plant_sample = PersistPlantSample(persistence)
    start_degradation_demo = StartDegradationDemo(
        HttpxSimulatorDemoGateway(settings.simulator_base_url)
    )
    plant_telemetry = AsyncUaPlantTelemetryAdapter(
        settings.opcua_endpoint,
        persist_plant_sample,
    )
    collector = OpcUaCollectorWorker(settings, plant_telemetry)
    return AppContainer(
        settings=settings,
        persist_plant_sample=persist_plant_sample,
        start_degradation_demo=start_degradation_demo,
        plant_telemetry=plant_telemetry,
        opcua_collector_worker=collector,
    )
