"""Subscribe to plant tags and forward samples to a callback."""

import logging
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from typing import Any

from asyncua import Client, Node
from asyncua.common.subscription import DataChangeNotif

from integrations.opcua.client import connect_client, disconnect_client
from integrations.opcua.node_map import MappedTag, plant_tags_for_equipment, resolve_namespace_index

logger = logging.getLogger(__name__)

SampleCallback = Callable[[datetime, str, str, float | str, str], Awaitable[None]]


class _PlantHandler:
    def __init__(
        self,
        node_to_tag: dict[str, MappedTag],
        on_sample: SampleCallback,
    ) -> None:
        self._node_to_tag = node_to_tag
        self._on_sample = on_sample

    async def datachange_notification(
        self, node: Node, val: Any, _data: DataChangeNotif
    ) -> None:
        tag = self._node_to_tag.get(node.nodeid.to_string())
        if tag is None:
            return
        ts = datetime.now(UTC)
        await self._on_sample(ts, tag.equipment_id, tag.tag_name, val, tag.unit)


async def _resolve_plant_nodes(client: Client, ns_idx: int) -> tuple[list[Node], dict[str, MappedTag]]:
    objects = client.nodes.objects
    plant = await objects.get_child(f"{ns_idx}:Plant")
    pump = await plant.get_child(f"{ns_idx}:PUMP-01")
    nodes: list[Node] = []
    node_to_tag: dict[str, MappedTag] = {}
    for mapped in plant_tags_for_equipment():
        node = await pump.get_child(f"{ns_idx}:{mapped.opc_name}")
        nodes.append(node)
        node_to_tag[node.nodeid.to_string()] = mapped
    return nodes, node_to_tag


class PlantSubscriber:
    def __init__(self, endpoint: str, on_sample: SampleCallback) -> None:
        self._endpoint = endpoint
        self._on_sample = on_sample
        self._client: Client | None = None
        self._subscription = None

    async def start(self, period_ms: int = 1000) -> None:
        self._client = await connect_client(self._endpoint)
        assert self._client is not None
        ns = await self._client.get_namespace_array()
        ns_idx = resolve_namespace_index(list(ns))
        nodes, node_to_tag = await _resolve_plant_nodes(self._client, ns_idx)
        handler = _PlantHandler(node_to_tag, self._on_sample)
        self._subscription = await self._client.create_subscription(period_ms, handler)
        await self._subscription.subscribe_data_change(nodes)
        logger.info("Subscribed to %d plant tags", len(nodes))

    async def stop(self) -> None:
        if self._subscription:
            await self._subscription.delete()
            self._subscription = None
        await disconnect_client(self._client)
        self._client = None
