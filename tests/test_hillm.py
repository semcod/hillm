from __future__ import annotations

import json

import pytest

from hillm.compat import agent_backend_aliases, is_hardware_device, tool_registry_entries
from hillm.controller import actuate_device, connect_device, read_device, write_device
from hillm.registry import detect_devices, get_device_spec, normalize_device_id
from hillm.validation import ecosystem_status, validate_device_readiness


def test_registry_lists_hardware_profiles() -> None:
    devices = detect_devices()
    assert len(devices) >= 10
    ids = {row["id"] for row in devices}
    assert "camera-usb" in ids
    assert "modbus-rtu" in ids
    assert "display-primary" in ids


def test_normalize_device_aliases() -> None:
    assert normalize_device_id("mic") == "microphone-default"
    assert normalize_device_id("modbus") == "modbus-rtu"


def test_dry_run_read_and_write() -> None:
    result = read_device("sensor-temp", dry_run=True)
    assert result.ok
    assert result.device_id == "sensor-temp"
    assert result.value is not None

    written = write_device("actuator-relay", "1", dry_run=True)
    assert written.ok
    assert written.value == "1"


def test_connect_and_actuate_dry_run() -> None:
    connected = connect_device("serial-ttyusb0", dry_run=True)
    assert connected.ok

    captured = actuate_device("camera-usb", "capture", dry_run=True)
    assert captured.ok


def test_validate_unknown_device() -> None:
    result = validate_device_readiness("missing-device")
    assert not result.ok
    assert result.errors


def test_ecosystem_status() -> None:
    status = ecosystem_status()
    assert status["ok"] is True
    assert status["devices_registered"] >= 10
    assert "scan" in status


def test_compat_exports_koru_registry_rows() -> None:
    aliases = agent_backend_aliases()
    assert aliases["hillm_shell"] == "hardware_device_cli"
    entries = tool_registry_entries()
    assert any(entry["id"] == "camera-usb" for entry in entries)
    assert is_hardware_device("camera-usb")
    assert get_device_spec("missing") is None


def test_dsl2hillm_health_dispatch() -> None:
    dsl2hillm = pytest.importorskip("dsl2hillm")
    result = dsl2hillm.dispatch("HEALTH")
    assert result.ok
    assert result.verb == "HEALTH"
    payload = json.loads(result.output)
    assert payload["package"] == "hillm"


def test_dsl2hillm_read_device_dispatch() -> None:
    dsl2hillm = pytest.importorskip("dsl2hillm")
    result = dsl2hillm.dispatch("READ DEVICE sensor-temp DRY_RUN true")
    assert result.ok
    assert result.data["device_id"] == "sensor-temp"


def test_nlp2hillm_maps_camera_prompt() -> None:
    nlp = pytest.importorskip("nlp2hillm.to_dsl")
    line = nlp.to_dsl("capture image from camera")
    assert "ACTUATE" in line or "READ" in line
    assert "camera" in line


def test_uri2hillm_decodes_query() -> None:
    uri2hillm = pytest.importorskip("uri2hillm.decode")
    line = uri2hillm.uri_to_dsl("hillm://cmd/READ?device=camera-usb&dry_run=true")
    assert line == "READ DEVICE camera-usb DRY_RUN true"
