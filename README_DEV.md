# HA Hikvision Intercom - Developer Guide

This document explains how to set up the development environment for the project.

---

# Requirements

- Python 3.14
- Git
- Visual Studio Code

Recommended VS Code extensions:

- Python
- Pylance
- Ruff

---

# Clone the repository

```bash
git clone https://github.com/JeanCoqs/ha-hikvision-intercom.git
cd ha-hikvision-intercom
```

---

# Create the virtual environment

Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

# Install development dependencies

```bash
pip install -r requirements.txt
```

---

# VS Code

Use the Python interpreter located in:

```
.venv
```

Project settings are stored in:

```
.vscode/settings.json
```

---

# Code Style

The project follows:

- Ruff
- Format on Save
- PEP8
- Type Hints

Always format the code before committing.

---

# Git Workflow

Create small commits.

Each commit should represent a completed milestone.

Example:

```
feat: validate Hikvision connection during config flow
```

Avoid commits that simply list modified files.

---

# Project Architecture

```
custom_components/
└── hikvision_intercom/
    ├── __init__.py
    ├── manifest.json
    ├── config_flow.py
    ├── const.py
    ├── client.py
    ├── api.py
    ├── exceptions.py
```

Responsibilities:

- client.py
    HTTP communication

- api.py
    Hikvision ISAPI endpoints

- config_flow.py
    Home Assistant configuration

- exceptions.py
    Custom exceptions

---

# Development Roadmap

Current milestone

✔ Integration skeleton

Next milestone

☐ Validate connection to Hikvision device

Future milestones

☐ Live Video

☐ Unlock Door

☐ Ring Sensor

☐ Answer Call

☐ Reject Call

☐ Hang Up

☐ Camera Entity

☐ Button Entities

☐ HACS Release

---

# Project Goals

The objective of this project is to create a native Home Assistant integration for Hikvision intercom devices.

The integration should:

- support multiple devices
- avoid proprietary SDKs
- communicate using ISAPI
- follow Home Assistant architecture and coding standards
- be suitable for publication on HACS