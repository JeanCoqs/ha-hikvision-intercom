"""Hikvision ISAPI event listener."""

from __future__ import annotations

import asyncio
import logging

import httpx

_LOGGER = logging.getLogger(__name__)


class HikvisionEventListener:
    """Listen for Hikvision ISAPI events."""

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
    ) -> None:

        self._host = host
        self._username = username
        self._password = password

        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        """Start listener."""

        self._task = asyncio.create_task(
            self._listen()
        )

    async def stop(self) -> None:
        """Stop listener."""

        if self._task:
            self._task.cancel()

    async def _listen(self) -> None:

        while True:

            try:

                async with httpx.AsyncClient(
                    timeout=None,
                ) as client:

                    async with client.stream(
                        "GET",
                        f"http://{self._host}/ISAPI/Event/notificationAlertStream",
                        auth=httpx.DigestAuth(
                            self._username,
                            self._password,
                        ),
                    ) as response:
                        if response.status_code != 200:
                            _LOGGER.warning(
                                "Event stream not available (%s)",
                                response.status_code,
                            )
                            return

                        async for line in response.aiter_lines():

                            if line:

                                _LOGGER.warning(line)

            except Exception as err:

                _LOGGER.exception(err)

                await asyncio.sleep(5)