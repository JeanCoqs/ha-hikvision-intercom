"""HTTP client for Hikvision ISAPI."""

from __future__ import annotations

import asyncio

import httpx

from .exceptions import (
    HikvisionAuthenticationError,
    HikvisionConnectionError,
)

DEFAULT_TIMEOUT = 10.0


class HikvisionClient:
    """HTTP client for Hikvision ISAPI."""

    def __init__(
        self,
        client: httpx.AsyncClient,
        host: str,
        port: int,
        username: str,
        password: str,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Initialize the client."""

        self._client = client
        self._base_url = f"http://{host}:{port}"
        self._auth = httpx.DigestAuth(username, password)
        self._timeout = timeout

    async def _request(
        self,
        method: str,
        path: str,
        *,
        body: str | None = None,
        content_type: str = "application/json",
    ) -> str:
        """Execute an HTTP request."""

        try:
            async with asyncio.timeout(self._timeout):
                response = await self._client.request(
                    method,
                    f"{self._base_url}{path}",
                    auth=self._auth,
                    content=body,
                    headers={
                        "Content-Type": content_type,
                    },
                )

        except (httpx.RequestError, TimeoutError) as err:
            raise HikvisionConnectionError from err

        if response.status_code in (401, 403):
            raise HikvisionAuthenticationError

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            raise HikvisionConnectionError from err

        return response.text

    #
    # ------------------------------------------------------------------
    # HTTP verbs
    # ------------------------------------------------------------------
    #

    async def get(self, path: str) -> str:
        """Execute a GET request."""

        return await self._request(
            "GET",
            path,
        )

    async def post(
        self,
        path: str,
        body: str,
        *,
        content_type: str = "application/json",
    ) -> str:
        """Execute a POST request."""

        return await self._request(
            "POST",
            path,
            body=body,
            content_type=content_type,
        )

    async def put(
        self,
        path: str,
        body: str,
        *,
        content_type: str = "application/json",
    ) -> str:
        """Execute a PUT request."""

        return await self._request(
            "PUT",
            path,
            body=body,
            content_type=content_type,
        )

    async def delete(self, path: str) -> str:
        """Execute a DELETE request."""

        return await self._request(
            "DELETE",
            path,
        )
