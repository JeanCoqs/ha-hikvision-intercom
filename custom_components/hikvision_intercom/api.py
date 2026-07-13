"""Hikvision ISAPI API."""

from __future__ import annotations

import json

from .client import HikvisionClient


class HikvisionAPI:
    """High level Hikvision ISAPI API."""

    def __init__(self, client: HikvisionClient) -> None:
        """Initialize the API."""

        self._client = client

    async def get_system_status(self) -> str:
        """Return system status."""

        return await self._client.get("/ISAPI/System/status")

    async def get_device_info(self) -> str:
        """Return device information."""

        return await self._client.get("/ISAPI/System/deviceInfo")

    async def get_call_status(self) -> str:
        """Return current call status."""

        return await self._client.get("/ISAPI/VideoIntercom/callStatus?format=json")

    async def get_caller_info(self) -> str:
        """Return caller information."""

        return await self._client.get("/ISAPI/VideoIntercom/callerInfo?format=json")

    async def answer_call(self) -> str:
        """Answer an incoming call."""

        payload = {
            "CallSignal": {
                "cmdType": "answer",
            }
        }

        return await self._client.put(
            "/ISAPI/VideoIntercom/callSignal?format=json",
            json.dumps(payload),
        )
