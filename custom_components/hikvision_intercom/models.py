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

    hardware_version: str

    firmware_release_date: str

    production_date: str

    mac_address: str

    device_type: str

    sub_device_type: str

    release_region: str

    bsp_version: str

    dsp_version: str
