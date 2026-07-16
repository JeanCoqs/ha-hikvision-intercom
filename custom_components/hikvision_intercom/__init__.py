"""The Hikvision Intercom integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_USERNAME,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.httpx_client import get_async_client
# from .event_listener import HikvisionEventListener
from .api import HikvisionAPI
from .client import HikvisionClient
from .const import (
    CONF_PORT,
    DOMAIN,
)
from .services import async_register_services
PLATFORMS = [
    "binary_sensor",
    "button",
    "camera",
]

type HikvisionConfigEntry = ConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HikvisionConfigEntry,
) -> bool:
    """Set up Hikvision Intercom from a config entry."""

    client = HikvisionClient(
        client=get_async_client(hass),
        host=entry.data[CONF_HOST],
        port=entry.data[CONF_PORT],
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
    )

    api = HikvisionAPI(client)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = api

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )
    if not hass.services.has_service(
        DOMAIN,
        "debug_request",
    ):
        await async_register_services(hass)
        
#    listener = HikvisionEventListener(
#        host=entry.data[CONF_HOST],
#        username=entry.data[CONF_USERNAME],
#        password=entry.data[CONF_PASSWORD],
#    )#
#
#    await listener.start()
#
#    hass.data[DOMAIN][f"{entry.entry_id}_listener"] = listener

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: HikvisionConfigEntry,
) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    listener = hass.data[DOMAIN].pop(
        f"{entry.entry_id}_listener",
        None,
    )

    if listener:
        await listener.stop()

    return unload_ok


