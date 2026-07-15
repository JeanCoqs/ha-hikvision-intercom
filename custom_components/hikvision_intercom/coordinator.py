"""DataUpdateCoordinator for Hikvision Intercom."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from .api import HikvisionAPI
from .models import DeviceInfo
from .parsers import parse_device_info

_LOGGER = logging.getLogger(__name__)


class HikvisionCoordinator(DataUpdateCoordinator[DeviceInfo]):
    """Coordinator for Hikvision Intercom."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: HikvisionAPI,
    ) -> None:
        """Initialize coordinator."""

        super().__init__(
            hass,
            logger=_LOGGER,
            name="hikvision_intercom",
            update_interval=timedelta(minutes=5),
        )

        self.api = api

    async def _async_update_data(self) -> DeviceInfo:
        """Fetch latest device information."""

        xml = await self.api.get_device_info()

        return parse_device_info(xml)
