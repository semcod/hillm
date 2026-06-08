"""Transport registry and resolution."""

from __future__ import annotations

from hillm.contracts.device import DeviceResult, HardwareTransport


def get_transport(transport_id: str) -> HardwareTransport:
    from hillm.transports.dry_run import DryRunTransport

    registry: dict[str, HardwareTransport] = {
        "dry_run": DryRunTransport(),
    }

    if transport_id == "serial":
        from hillm.transports.serial import SerialTransport

        registry["serial"] = SerialTransport()
    elif transport_id == "modbus":
        from hillm.transports.modbus import ModbusTransport

        registry["modbus"] = ModbusTransport()
    elif transport_id == "mqtt":
        from hillm.transports.mqtt import MqttTransport

        registry["mqtt"] = MqttTransport()
    elif transport_id == "http":
        from hillm.transports.http_device import HttpDeviceTransport

        registry["http"] = HttpDeviceTransport()
    elif transport_id == "v4l":
        from hillm.transports.v4l import V4lTransport

        registry["v4l"] = V4lTransport()
    elif transport_id == "display":
        from hillm.transports.display import DisplayTransport

        registry["display"] = DisplayTransport()
    elif transport_id == "audio":
        from hillm.transports.audio import AudioTransport

        registry["audio"] = AudioTransport()
    elif transport_id == "input":
        from hillm.transports.input import InputTransport

        registry["input"] = InputTransport()
    elif transport_id == "usb":
        from hillm.transports.usb import UsbTransport

        registry["usb"] = UsbTransport()

    backend = registry.get(transport_id)
    if backend is None:
        raise ValueError(f"unknown transport: {transport_id}")
    return backend


def unavailable_result(*, device_id: str, backend: str, message: str) -> DeviceResult:
    return DeviceResult(ok=False, device_id=device_id, backend=backend, error=message, message=message)
