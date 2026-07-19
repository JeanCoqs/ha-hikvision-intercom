"""Binary sensor platform for Hikvision Intercom."""

from __future__ import annotations

import json
import logging
from datetime import timedelta

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval

from .api import HikvisionAPI
from .const import (
    CONF_CALL_STATE_POLL,
    DEFAULT_CALL_STATE_POLL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Hikvision binary sensors."""

    api: HikvisionAPI = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            HikvisionRingingBinarySensor(
                api,
                entry,
            )
        ]
    )


class HikvisionRingingBinarySensor(BinarySensorEntity):
    """Binary sensor for intercom ringing."""

    _attr_has_entity_name = True
    _attr_device_class = BinarySensorDeviceClass.SOUND

    def __init__(
        self,
        api: HikvisionAPI,
        entry: ConfigEntry,
    ) -> None:
        """Initialize."""

        self._api = api
        self._entry = entry
        self._poll_interval = entry.data.get(
            CONF_CALL_STATE_POLL,
            DEFAULT_CALL_STATE_POLL,
        )

        self._attr_name = "Call"
        self._attr_unique_id = f"{entry.entry_id}_call"

        self._attr_is_on = False

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

    async def async_added_to_hass(self) -> None:
        """Start polling."""

        async def _poll(now) -> None:
            await self._async_update()

        self.async_on_remove(
            async_track_time_interval(
                self.hass,
                _poll,
                timedelta(seconds=self._poll_interval),
            )
        )

        await self._async_update()

    async def _async_update(self) -> None:
        """Read call status."""

        try:
            result = await self._api.get_call_status()
            data = json.loads(result)

            status = data.get("CallStatus", {}).get("status", "").lower()

            self._attr_is_on = status == "ring"

            self.async_write_ha_state()

        except Exception:
            _LOGGER.exception("Error reading call status")
