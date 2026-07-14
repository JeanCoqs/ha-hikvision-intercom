"""Config flow for the Hikvision Intercom integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_USERNAME,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.httpx_client import get_async_client

from .api import HikvisionAPI
from .client import HikvisionClient
from .const import (
    CONF_PORT,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DOMAIN,
)
from .exceptions import (
    HikvisionAuthenticationError,
    HikvisionConnectionError,
)
from .parsers import parse_device_info

_LOGGER = logging.getLogger(__name__)


async def validate_input(
    hass: HomeAssistant,
    data: dict[str, Any],
) -> tuple[dict[str, Any], str]:
    """Validate user input by connecting to the Hikvision device."""

    client = HikvisionClient(
        client=get_async_client(hass),
        host=data[CONF_HOST],
        port=data[CONF_PORT],
        username=data[CONF_USERNAME],
        password=data[CONF_PASSWORD],
    )

    api = HikvisionAPI(client)

    xml = await api.get_device_info()

    device = parse_device_info(xml)

    _LOGGER.info(
        "Connected to %s (%s) - Firmware %s",
        device.model,
        device.serial_number,
        device.firmware_version,
    )

    return (
        {
            "title": data[CONF_NAME],
        },
        device.serial_number,
    )


class HikvisionIntercomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hikvision Intercom."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ):
        """Handle the initial step."""

        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info, unique_id = await validate_input(
                    self.hass,
                    user_input,
                )

                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()

            except HikvisionAuthenticationError:
                errors["base"] = "invalid_auth"

            except HikvisionConnectionError:
                errors["base"] = "cannot_connect"

            except Exception:  # noqa: BLE001
                _LOGGER.exception("Unexpected error during configuration")
                errors["base"] = "unknown"

            else:
                return self.async_create_entry(
                    title=info["title"],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME,
                        default=DEFAULT_NAME,
                    ): str,
                    vol.Required(CONF_HOST): str,
                    vol.Required(
                        CONF_PORT,
                        default=DEFAULT_PORT,
                    ): int,
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )