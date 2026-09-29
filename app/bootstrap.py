from dataclasses import dataclass

from app.config import Settings
from app.db.store import SqlAlchemyTelemetryPersistence
from app.domain.ports import PlantTelemetryPort
from app.opcua.telemetry_adapter import AsyncUaPlantTelemetryAdapter
from app.services.degradation_demo import StartDegradationDemo
from app.services.persist_sample import PersistPlantSample
from app.simulator_client import HttpxSimulatorDemoGateway
from app.workers.opcua_collector_worker import OpcUaCollectorWorker


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
