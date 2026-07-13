"""The Hikvision Intercom integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.httpx_client import get_async_client

from .api import HikvisionAPI
from .client import HikvisionClient
from .const import (
    CONF_PORT,
    DOMAIN,
)

type HikvisionConfigEntry = ConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HikvisionConfigEntry,
) -> bool:
    """Set up Hikvision Intercom from a config entry."""

    http_client = get_async_client(hass)

    client = HikvisionClient(
        client=http_client,
        host=entry.data["host"],
        port=entry.data[CONF_PORT],
        username=entry.data["username"],
        password=entry.data["password"],
    )

    api = HikvisionAPI(client)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = api

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: HikvisionConfigEntry,
) -> bool:
    """Unload a config entry."""

    hass.data[DOMAIN].pop(entry.entry_id)

    return True
