from __future__ import annotations

from hillm.resolve import resolve_device_from_text


def test_resolve_temperature_serial() -> None:
    assert resolve_device_from_text("read temperature from serial") == "sensor-temp"


def test_resolve_mouse_over_usb() -> None:
    assert resolve_device_from_text("read usb port for mouse") == "mouse-default"
