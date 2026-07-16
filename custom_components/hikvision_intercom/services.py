"""Services for Hikvision Intercom."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant, ServiceCall
from .isapi_services import ISAPIExplorer
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_register_services(
    hass: HomeAssistant,
) -> None:
    """Register services."""

    async def handle_debug_request(
        call: ServiceCall,
    ) -> None:

        method = call.data["method"]
        endpoint = call.data["endpoint"]
        body = call.data.get("body")
        save = call.data.get("save", True)

        explorer = ISAPIExplorer(hass)

        for api in hass.data[DOMAIN].values():

            try:

                result = await api.request(
                    method=method,
                    endpoint=endpoint,
                    body=body,
                )

                if save:
                    filename = explorer.save(
                        method=method,
                        endpoint=endpoint,
                        data=result,
                    )

                    _LOGGER.warning(
                        "ISAPI %s %s -> %s",
                        method,
                        endpoint,
                        filename,
                    )

                else:

                    _LOGGER.warning(result)

            except Exception:

                _LOGGER.exception(
                    "ISAPI %s %s failed",
                    method,
                    endpoint,
                )



    hass.services.async_register(
        DOMAIN,
        "isapi_request",
        handle_debug_request,
    )