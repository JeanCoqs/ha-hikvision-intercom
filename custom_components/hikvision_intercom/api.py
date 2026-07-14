"""Hikvision ISAPI API."""

from __future__ import annotations

import json

from .client import HikvisionClient


class HikvisionAPI:
    """High level Hikvision ISAPI API."""

    def __init__(self, client: HikvisionClient) -> None:
        """Initialize the API."""

        self._client = client

    #
    # ------------------------------------------------------------------
    # System
    # ------------------------------------------------------------------
    #

    async def get_system_status(self) -> str:
        """Return system status."""

        return await self._client.get("/ISAPI/System/status")

    async def get_device_info(self) -> str:
        """Return device information."""

        return await self._client.get("/ISAPI/System/deviceInfo")

    #
    # ------------------------------------------------------------------
    # Video Intercom
    # ------------------------------------------------------------------
    #

    async def get_call_status(self) -> str:
        """Return current call status."""

        return await self._client.get("/ISAPI/VideoIntercom/callStatus?format=json")

    async def get_caller_info(self) -> str:
        """Return caller information."""

        return await self._client.get("/ISAPI/VideoIntercom/callerInfo?format=json")

    async def _call_signal(self, command: str) -> str:
        """Send a call signal command."""

        payload = {
            "CallSignal": {
                "cmdType": command,
            }
        }

        return await self._client.put(
            "/ISAPI/VideoIntercom/callSignal?format=json",
            body=json.dumps(payload),
        )

    async def answer_call(self) -> str:
        """Answer an incoming call."""

        return await self._call_signal("answer")

    async def reject_call(self) -> str:
        """Reject an incoming call."""

        return await self._call_signal("reject")

    async def hangup_call(self) -> str:
        """Hang up the current call."""

        return await self._call_signal("hangup")

    #
    # ------------------------------------------------------------------
    # Access Control
    # ------------------------------------------------------------------
    #

    async def unlock_door(
        self,
        door: int = 1,
        command: str = "open",
    ) -> str:
        """Unlock a door."""

        body = f"""<?xml version="1.0" encoding="utf-8"?>
<RemoteControlDoor xmlns="http://www.isapi.org/ver20/XMLSchema" version="2.0">
    <cmd>{command}</cmd>
</RemoteControlDoor>
"""

        return await self._client.put(
            f"/ISAPI/AccessControl/RemoteControl/door/{door}",
            body=body,
            content_type="application/xml",
        )

    #
    # ------------------------------------------------------------------
    # Streaming
    # ------------------------------------------------------------------
    #

    async def get_streaming_channel(
        self,
        channel: int = 101,
    ) -> str:
        """Return streaming channel configuration."""

        return await self._client.get(f"/ISAPI/Streaming/channels/{channel}")

    #
    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    #

    async def get_event_log(
        self,
        max_results: int = 20,
    ) -> str:
        """Return access control event log."""

        payload = {
            "AcsEventCond": {
                "searchID": "homeassistant",
                "searchResultPosition": 0,
                "maxResults": max_results,
                "major": 0,
                "minor": 0,
                "timeReverseOrder": True,
            }
        }

        return await self._client.post(
            "/ISAPI/AccessControl/AcsEvent?format=json",
            body=json.dumps(payload),
        )

    async def notification_alert_stream(self) -> str:
        """Open notification alert stream."""

        return await self._client.get("/ISAPI/Event/notificationAlertStream")
