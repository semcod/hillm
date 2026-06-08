"""Platform hardware discovery."""

from __future__ import annotations

import os
import platform
import shutil
from typing import Any

from hillm.registry import detect_devices, iter_device_specs


def platform_summary() -> dict[str, Any]:
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python": platform.python_version(),
    }


def scan_host() -> dict[str, Any]:
    """Return a host-level inventory of known device profiles and OS hints."""
    dev_names = os.listdir("/dev") if os.path.isdir("/dev") else []
    hints: dict[str, Any] = {
        "serial_ports": sorted(
            f"/dev/{name}"
            for name in dev_names
            if "ttyUSB" in name or "ttyACM" in name or "ttyS" in name
        ),
        "video_nodes": sorted(
            f"/dev/{name}"
            for name in (os.listdir("/dev") if os.path.isdir("/dev") else [])
            if name.startswith("video")
        ),
        "tools": {
            "xrandr": shutil.which("xrandr"),
            "lsusb": shutil.which("lsusb"),
            "pactl": shutil.which("pactl"),
            "arecord": shutil.which("arecord"),
        },
    }
    return {
        "platform": platform_summary(),
        "hints": hints,
        "devices": detect_devices(),
    }
