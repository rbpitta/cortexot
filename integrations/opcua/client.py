"""Thin asyncua client helpers."""

import logging

from asyncua import Client

logger = logging.getLogger(__name__)


async def connect_client(endpoint: str) -> Client:
    client = Client(url=endpoint)
    client.session_timeout = 60000
    await client.connect()
    logger.info("OPC-UA connected to %s", endpoint)
    return client


async def disconnect_client(client: Client | None) -> None:
    if client is None:
        return
    try:
        await client.disconnect()
    except Exception:
        logger.exception("OPC-UA disconnect error")
