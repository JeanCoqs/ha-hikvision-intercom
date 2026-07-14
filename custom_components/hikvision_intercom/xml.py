"""XML builders for Hikvision ISAPI."""

from __future__ import annotations

ISAPI_NAMESPACE = "http://www.isapi.org/ver20/XMLSchema"


def build_remote_control_door(cmd: str) -> str:
    """Build the XML payload for remote door control."""

    return f"""<?xml version="1.0" encoding="utf-8"?>
<RemoteControlDoor xmlns="{ISAPI_NAMESPACE}" version="2.0">
    <cmd>{cmd}</cmd>
</RemoteControlDoor>
"""
