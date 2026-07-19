"""Camera platform for Hikvision Intercom."""

from __future__ import annotations

from homeassistant.components.camera import (
    Camera,
    CameraEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import HikvisionAPI
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Hikvision camera."""

    api: HikvisionAPI = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            HikvisionCamera(api, entry),
        ]
    )


class HikvisionCamera(Camera):
    """Hikvision RTSP Camera."""

    _attr_has_entity_name = True

    def __init__(
        self,
        api: HikvisionAPI,
        entry: ConfigEntry,
    ) -> None:
        """Initialize camera."""

        super().__init__()

        self._api = api
        self._entry = entry

        self._attr_name = "Camera"
        self._attr_unique_id = f"{entry.entry_id}_camera"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""

        return DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    self._entry.entry_id,
                )
            },
            name=self._entry.title,
            manufacturer="Hikvision",
        )

    async def stream_source(self) -> str:
        """Return RTSP stream."""

        host = self._entry.data[CONF_HOST]
        username = self._entry.data[CONF_USERNAME]
        password = self._entry.data[CONF_PASSWORD]

        return f"rtsp://{username}:{password}@{host}:554/Streaming/Channels/101"

    async def async_camera_image(self, width=None, height=None):
        """Return camera snapshot."""

        return await self._api.get_snapshot()

    @property
    def supported_features(self) -> CameraEntityFeature:
        """Supported camera features."""

        return CameraEntityFeature.STREAM
