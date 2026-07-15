"""Helpers for Home Assistant Device Registry."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN
from .models import DeviceInfo as HikvisionDeviceInfo


def build_device_info(
    device: HikvisionDeviceInfo,
    name: str,
) -> DeviceInfo:
    """Build Home Assistant DeviceInfo."""

    return DeviceInfo(
        identifiers={
            (
                DOMAIN,
                device.serial_number,
            )
        },
        manufacturer="Hikvision",
        model=device.model,
        name=name,
        serial_number=device.serial_number,
        sw_version=device.firmware_version,
        hw_version=getattr(device, "hardware_version", None),
        connections={
            (
                "mac",
                device.mac_address,
            )
        }
        if device.mac_address
        else set(),
    )
