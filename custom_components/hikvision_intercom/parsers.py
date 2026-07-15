"""Parsers for Hikvision ISAPI responses."""

from __future__ import annotations

import xml.etree.ElementTree as ET

from .models import DeviceInfo

_ISAPI_NAMESPACE = {
    "isapi": "http://www.isapi.org/ver20/XMLSchema",
}


def _text(
    root: ET.Element,
    tag: str,
    default: str = "",
) -> str:
    """Return the text of an ISAPI XML element."""

    return root.findtext(
        f"isapi:{tag}",
        default=default,
        namespaces=_ISAPI_NAMESPACE,
    )


def parse_device_info(xml: str) -> DeviceInfo:
    """Parse the ISAPI DeviceInfo XML response."""

    root = ET.fromstring(xml)

    return DeviceInfo(
        device_name=_text(root, "deviceName", "Hikvision"),
        serial_number=_text(root, "serialNumber"),
        model=_text(root, "model", "Unknown"),
        firmware_version=_text(root, "firmwareVersion", "Unknown"),
        hardware_version=_text(root, "hardwareVersion"),
        firmware_release_date=_text(root, "firmwareReleasedDate"),
        production_date=_text(root, "productionDate"),
        mac_address=_text(root, "macAddress"),
        device_type=_text(root, "deviceType"),
        sub_device_type=_text(root, "subDeviceType"),
        release_region=_text(root, "releaseRegion"),
        bsp_version=_text(root, "bspVersion"),
        dsp_version=_text(root, "dspVersion"),
    )
