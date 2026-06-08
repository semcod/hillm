"""Resolve natural-language or alias hints to registry device ids."""

from __future__ import annotations

import re

from hillm.registry import get_device_spec, normalize_device_id

_DEVICE_HINTS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\b(mouse|mysz(?:ka|ki)?)\b", re.I), "mouse-default"),
    (re.compile(r"\b(keyboard|klawiatur(?:a|y|ę|e)?)\b", re.I), "keyboard-default"),
    (re.compile(r"\b(camera|webcam)\b", re.I), "camera-usb"),
    (re.compile(r"\b(microphone|mic)\b", re.I), "microphone-default"),
    (re.compile(r"\b(speaker)\b", re.I), "speaker-default"),
    (re.compile(r"\b(relay)\b", re.I), "actuator-relay"),
    (re.compile(r"\b(modbus)\b", re.I), "modbus-rtu"),
    (re.compile(r"\b(mqtt)\b", re.I), "mqtt-broker"),
    (re.compile(r"\b(hdmi)\b", re.I), "hdmi-out"),
    (re.compile(r"\b(display)\b", re.I), "display-primary"),
    (re.compile(r"\b(temp|temperature|sensor)\b", re.I), "sensor-temp"),
    (re.compile(r"\b(serial|rs232|rs485)\b", re.I), "__serial__"),
    (re.compile(r"\b(usb)\b", re.I), "usb-hub"),
)


def default_serial_device() -> str:
    for device_id in ("serial-ttyacm0", "serial-ttyusb0"):
        spec = get_device_spec(device_id)
        if spec and spec.to_dict().get("detected"):
            return device_id
    return "serial-ttyusb0"


def resolve_device_from_text(prompt: str) -> str:
    """Map NL keywords or aliases to a registered device id."""
    text = prompt.strip()
    lowered = text.lower()
    if "temperature" in lowered or "temp" in lowered:
        if re.search(r"\b(serial|rs232|rs485)\b", text, re.I):
            return "sensor-temp"
    for pattern, device_id in _DEVICE_HINTS:
        if not pattern.search(text):
            continue
        if device_id == "__serial__":
            return default_serial_device()
        resolved = normalize_device_id(device_id)
        if get_device_spec(resolved):
            return resolved
    fallback = normalize_device_id(text)
    if get_device_spec(fallback):
        return fallback
    return default_serial_device()
