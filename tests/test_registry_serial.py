from __future__ import annotations

from hillm.registry import first_existing_serial_path, get_device_spec


def test_first_existing_serial_path_prefers_order(monkeypatch) -> None:
    def fake_exists(path: str) -> bool:
        return path in {"/dev/ttyACM0", "/dev/ttyUSB1"}

    monkeypatch.setattr("os.path.exists", fake_exists)
    assert first_existing_serial_path("/dev/ttyUSB0", "/dev/ttyACM0", "/dev/ttyUSB1") == "/dev/ttyACM0"


def test_sensor_temp_falls_back_to_ttyacm(monkeypatch) -> None:
    spec = get_device_spec("sensor-temp")
    assert spec is not None

    def fake_exists(path: str) -> bool:
        return path == "/dev/ttyACM0"

    monkeypatch.setattr("os.path.exists", fake_exists)
    assert spec.resolve_address() == "/dev/ttyACM0"


def test_sensor_temp_keeps_configured_when_present(monkeypatch) -> None:
    spec = get_device_spec("sensor-temp")
    assert spec is not None

    def fake_exists(path: str) -> bool:
        return path in {"/dev/ttyUSB0", "/dev/ttyACM0"}

    monkeypatch.setattr("os.path.exists", fake_exists)
    assert spec.resolve_address() == "/dev/ttyUSB0"


def test_sensor_temp_env_override_wins(monkeypatch) -> None:
    spec = get_device_spec("sensor-temp")
    assert spec is not None
    monkeypatch.setenv("HILLM_SENSOR_TEMP_ADDRESS", "/dev/ttyUSB2")
    monkeypatch.setattr("os.path.exists", lambda _path: False)
    assert spec.resolve_address() == "/dev/ttyUSB2"
