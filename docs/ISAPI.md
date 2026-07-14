# Hikvision ISAPI Reference

This document collects the ISAPI endpoints discovered during the development of the Home Assistant Hikvision Intercom integration.

The purpose is to document:

- endpoint
- HTTP method
- payload
- response
- implementation status

---

# System

## Device Information

| Property | Value |
|----------|-------|
| Endpoint | `/ISAPI/System/deviceInfo` |
| Method | `GET` |
| Status | ✅ Implemented |

Returns the device information as XML.

Example response:

```xml
<DeviceInfo>
    <deviceName>...</deviceName>
    <model>...</model>
    <serialNumber>...</serialNumber>
</DeviceInfo>
```

Used for:

- Config Flow
- Device Registry
- Unique ID

---

## System Status

| Property | Value |
|----------|-------|
| Endpoint | `/ISAPI/System/status` |
| Method | `GET` |
| Status | ✅ Implemented |

Returns the current device status.

---

# Video Intercom

## Call Status

| Property | Value |
|----------|-------|
| Endpoint | `/ISAPI/VideoIntercom/callStatus?format=json` |
| Method | `GET` |
| Status | 🚧 Planned |

Returns the current call status.

---

## Caller Information

| Property | Value |
|----------|-------|
| Endpoint | `/ISAPI/VideoIntercom/callerInfo?format=json` |
| Method | `GET` |
| Status | 🚧 Planned |

Returns information about the current caller.

---

## Answer Call

| Property | Value |
|----------|-------|
| Endpoint | `/ISAPI/VideoIntercom/callSignal?format=json` |
| Method | `PUT` |
| Status | ✅ Implemented |

Payload

```json
{
    "CallSignal": {
        "cmdType": "answer"
    }
}
```

---

# Access Control

## Unlock Door

| Property | Value |
|----------|-------|
| Endpoint | `/ISAPI/AccessControl/RemoteControl/door/1` |
| Method | `PUT` |
| Status | 🚧 Planned |

Content-Type

```
application/xml
```

Payload

```xml
<?xml version="1.0" encoding="utf-8"?>
<RemoteControlDoor
    xmlns="http://www.isapi.org/ver20/XMLSchema"
    version="2.0">
    <cmd>resume</cmd>
</RemoteControlDoor>
```

Expected response

```xml
<ResponseStatus>
    <statusString>OK</statusString>
</ResponseStatus>
```

---

# Streaming

## Channel Information

| Property | Value |
|----------|-------|
| Endpoint | `/ISAPI/Streaming/channels/101` |
| Method | `GET` |
| Status | ✅ Documented |

Returns the configuration of the main video stream.

Discovered capabilities:

- H.264
- 1920 × 1080
- Progressive
- JPEG snapshots
- RTSP
- HTTP streaming
- G.711 μ-law audio

---

# Future endpoints

To be discovered

- Snapshot
- Live HTTP stream
- RTSP stream URL
- Reject Call
- Hang Up
- Ring Event
- Door Status
- Motion Event
- Tamper Event

---

# Notes

This document is built by observing the native Hikvision web interface using the browser Developer Tools.

Only endpoints verified on real devices are documented here.