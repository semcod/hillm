from __future__ import annotations

import re

from hillm.registry import normalize_device_id


_READ_RE = re.compile(r"\b(read|odczytaj|pobierz)\b", re.I)
_WRITE_RE = re.compile(r"\b(write|zapisz|ustaw)\b", re.I)
_CONNECT_RE = re.compile(r"\b(connect|polacz|połącz)\b", re.I)
_ACTUATE_RE = re.compile(r"\b(actuate|capture|snapshot|mute|unmute|enable|disable)\b", re.I)
_DEVICE_RE = re.compile(
    r"\b(camera|display|hdmi|serial|modbus|mqtt|speaker|microphone|mic|usb|relay|keyboard|mouse)\b",
    re.I,
)


def to_dsl(prompt: str) -> str:
    text = prompt.strip()
    if not text:
        raise ValueError("empty prompt")
    upper = text.upper()
    if upper in {"HEALTH", "DEVICES", "ORIENT", "ACTIONS"}:
        return upper
    device_match = _DEVICE_RE.search(text)
    device = normalize_device_id(device_match.group(1).lower()) if device_match else "serial-ttyusb0"
    if _CONNECT_RE.search(text):
        return f"CONNECT DEVICE {device}"
    if _WRITE_RE.search(text):
        value = "on"
        if "off" in text.lower():
            value = "off"
        return f'WRITE DEVICE {device} VALUE {value}'
    if _ACTUATE_RE.search(text):
        action = "capture" if "camera" in text.lower() else "on"
        return f"ACTUATE DEVICE {device} ACTION {action}"
    register = "temperature" if "temp" in text.lower() else ""
    if register:
        return f"READ DEVICE {device} REGISTER {register}"
    return f"READ DEVICE {device}"
