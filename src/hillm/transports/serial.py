"""Serial / RS232 / RS485 transport."""

from __future__ import annotations

from typing import Any

from hillm.contracts.device import DeviceResult
from hillm.registry import first_existing_serial_path


def _serial_error_hint(exc: Exception, *, address: str = "") -> str:
    msg = str(exc)
    if "No such file or directory" in msg or "could not open port" in msg:
        available = first_existing_serial_path(
            "/dev/ttyACM0",
            "/dev/ttyUSB0",
            "/dev/ttyUSB1",
            "/dev/ttyS0",
        )
        hint = "use DRY_RUN true or export HILLM_DRY_RUN=1"
        if available:
            hint = f"try HILLM_<DEVICE_ID>_ADDRESS={available} or {hint}"
        elif address:
            hint = f"set HILLM_<DEVICE_ID>_ADDRESS (configured: {address}) or {hint}"
        return f"{msg} (hint: {hint})"
    return msg


class SerialTransport:
    transport_id = "serial"

    def available(self) -> bool:
        try:
            import serial  # noqa: F401

            return True
        except ImportError:
            return False

    def _open(self, address: str, **options: Any):
        import serial

        baudrate = int(options.get("baudrate", 9600))
        timeout = float(options.get("timeout", 1.0))
        return serial.Serial(port=address, baudrate=baudrate, timeout=timeout)

    def connect(self, *, address: str, **options: Any) -> DeviceResult:
        if not self.available():
            return DeviceResult(
                ok=False,
                backend=self.transport_id,
                error="pyserial not installed; pip install 'hillm[serial]'",
            )
        try:
            port = self._open(address, **options)
            port.close()
            return DeviceResult(ok=True, backend=self.transport_id, message=f"serial port openable: {address}")
        except Exception as exc:
            return DeviceResult(ok=False, backend=self.transport_id, error=_serial_error_hint(exc, address=address))

    def disconnect(self, *, address: str, **options: Any) -> DeviceResult:
        return DeviceResult(ok=True, backend=self.transport_id, message=f"serial disconnected: {address}")

    def read(self, *, address: str, register: str = "", **options: Any) -> DeviceResult:
        if not self.available():
            return DeviceResult(ok=False, backend=self.transport_id, error="pyserial not installed")
        try:
            with self._open(address, **options) as port:
                size = int(options.get("size", 64))
                data = port.read(size)
            return DeviceResult(
                ok=True,
                backend=self.transport_id,
                value=data.decode("utf-8", errors="replace"),
                data={"raw_bytes": len(data), "register": register},
            )
        except Exception as exc:
            return DeviceResult(ok=False, backend=self.transport_id, error=_serial_error_hint(exc, address=address))

    def write(self, *, address: str, value: Any, register: str = "", **options: Any) -> DeviceResult:
        if not self.available():
            return DeviceResult(ok=False, backend=self.transport_id, error="pyserial not installed")
        try:
            payload = str(value).encode("utf-8")
            with self._open(address, **options) as port:
                written = port.write(payload)
            return DeviceResult(ok=True, backend=self.transport_id, value=written, data={"register": register})
        except Exception as exc:
            return DeviceResult(ok=False, backend=self.transport_id, error=_serial_error_hint(exc, address=address))

    def actuate(self, *, address: str, action: str, **params: Any) -> DeviceResult:
        command = params.get("command", action)
        return self.write(address=address, value=command, **params)

    def status(self, *, address: str, **options: Any) -> DeviceResult:
        import os

        exists = os.path.exists(address)
        return DeviceResult(
            ok=exists,
            backend=self.transport_id,
            message=f"serial path {'present' if exists else 'missing'}: {address}",
            data={"address": address, "exists": exists},
            error=None if exists else f"missing serial device: {address}",
        )
