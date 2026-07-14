"""Button platform for Hikvision Intercom."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
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
    """Set up Hikvision buttons."""

    api: HikvisionAPI = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            HikvisionUnlockDoorButton(
                api,
                entry,
                door=1,
            ),
        ]
    )


class HikvisionUnlockDoorButton(ButtonEntity):
    """Unlock door button."""

    _attr_has_entity_name = True

    def __init__(
        self,
        api: HikvisionAPI,
        entry: ConfigEntry,
        door: int,
    ) -> None:
        """Initialize button."""

        self._api = api
        self._entry = entry
        self._door = door

        self._attr_name = f"Unlock Door {door}"
        self._attr_unique_id = f"{entry.entry_id}_unlock_door_{door}"

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

    async def async_press(self) -> None:
        """Handle button press."""

        await self._api.unlock_door(
            door=self._door,
        )
