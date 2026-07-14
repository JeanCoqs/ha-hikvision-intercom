"""Parsers for Hikvision ISAPI responses."""

from __future__ import annotations

import xml.etree.ElementTree as ET

from .models import DeviceInfo

_ISAPI_NAMESPACE = {
    "isapi": "http://www.isapi.org/ver20/XMLSchema",
}


def parse_device_info(xml: str) -> DeviceInfo:
    """Parse the ISAPI DeviceInfo XML response."""

    root = ET.fromstring(xml)

    return DeviceInfo(
        device_name=root.findtext(
            "isapi:deviceName",
            default="Hikvision",
            namespaces=_ISAPI_NAMESPACE,
        ),
        serial_number=root.findtext(
            "isapi:serialNumber",
            default="",
            namespaces=_ISAPI_NAMESPACE,
        ),
        model=root.findtext(
            "isapi:model",
            default="Unknown",
            namespaces=_ISAPI_NAMESPACE,
        ),
        firmware_version=root.findtext(
            "isapi:firmwareVersion",
            default="Unknown",
            namespaces=_ISAPI_NAMESPACE,
        ),
        mac_address=root.findtext(
            "isapi:macAddress",
            default="",
            namespaces=_ISAPI_NAMESPACE,
        ),
    )