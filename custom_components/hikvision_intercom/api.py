"""Hikvision ISAPI API."""

from __future__ import annotations

import json
import logging

from .client import HikvisionClient

_LOGGER = logging.getLogger(__name__)


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

    async def request(
        self,
        method: str,
        endpoint: str,
        body: str | None = None,
    ) -> str:
        """Execute a raw ISAPI request."""

        method = method.upper()

        if method == "GET":
            return await self._client.get(endpoint)

        if method == "PUT":
            return await self._client.put(
                endpoint,
                body=body or "",
                content_type="application/xml",
            )

        if method == "POST":
            return await self._client.post(
                endpoint,
                body=body or "",
                content_type="application/json",
            )

        raise ValueError(f"Unsupported method: {method}")

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

        return await self._call_signal("cancel")

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
    # Streaming & snapshot
    # ------------------------------------------------------------------
    #

    async def get_streaming_channel(
        self,
        channel: int = 101,
    ) -> str:
        """Return streaming channel configuration."""

        return await self._client.get(f"/ISAPI/Streaming/channels/{channel}")

    async def get_snapshot(
        self,
        channel: int = 101,
    ) -> bytes:
        """Return a JPEG snapshot."""

        return await self._client.get_bytes(
            f"/ISAPI/Streaming/channels/{channel}/picture"
        )

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

    async def get_key_config(
        self,
        key: int = 1,
    ) -> str:
        """Return key configuration."""

        return await self._client.get(f"/ISAPI/VideoIntercom/keyCfg/{key}")

    async def reboot(self) -> str:
        """Reboot the device."""

        return await self._client.put(
            "/ISAPI/System/reboot",
            body="",
            content_type="application/xml",
        )

    async def get_audio_output(self) -> str:
        """Return audio output configuration."""

        return await self._client.get("/ISAPI/System/Audio/AudioOut/channels/1")

    async def get_io_capabilities(self) -> str:
        """Return IO capabilities."""

        return await self._client.get("/ISAPI/System/IO/capabilities")

    async def get_output_status(
        self,
        output: int = 1,
    ) -> str:
        """Return output status."""

        return await self._client.get(f"/ISAPI/System/IO/outputs/{output}")

    async def get_backlight(self) -> str:
        """Return backlight configuration."""

        return await self._client.get(
            "/ISAPI/VideoIntercom/SubModuleBacklight?format=json"
        )
