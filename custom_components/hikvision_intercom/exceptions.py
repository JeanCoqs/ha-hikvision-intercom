"""Exceptions for the Hikvision Intercom integration."""


class HikvisionError(Exception):
    """Base exception."""


class HikvisionConnectionError(HikvisionError):
    """Cannot connect to the device."""


class HikvisionAuthenticationError(HikvisionError):
    """Authentication failed."""
