"""Data models for Hikvision Intercom."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DeviceInfo:
    """Hikvision device information."""

    device_name: str
    serial_number: str
    model: str
    firmware_version: str
    mac_address: str