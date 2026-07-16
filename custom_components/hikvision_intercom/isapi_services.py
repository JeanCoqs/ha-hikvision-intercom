"""ISAPI Explorer."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET


class ISAPIExplorer:

    def __init__(self, hass) -> None:
        self._hass = hass

    def format(self, data: str) -> str:
        """Pretty print XML when possible."""

        try:
            root = ET.fromstring(data)
            ET.register_namespace(
                "",
                "http://www.isapi.org/ver20/XMLSchema",
            )
            ET.indent(root, space="  ")
            return ET.tostring(
                root,
                encoding="unicode",
                xml_declaration=True,
            )

        except Exception:
            return data

    def save(
        self,
        method: str,
        endpoint: str,
        data: str,
    ) -> Path:
        """Save response to file."""

        folder = Path(
            self._hass.config.path(
                "hikvision_intercom",
                "debug",
            )
        )

        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


        extension = ".xml"
        content = data.lstrip()
        if content.startswith("{") or content.startswith("["):
            extension = ".json"
        filename = (
            endpoint.strip("/")
            .replace("/", "_")
            .replace("?", "_")
            .replace("&", "_")
            .replace("=", "_")
        )
        path = folder / (
            f"{timestamp}_{method.upper()}_{filename}{extension}"
        )

        path.write_text(
            self.format(data),
            encoding="utf-8",
        )

        return path