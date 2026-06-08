"""USB device enumeration transport."""

from __future__ import annotations

import shutil
import subprocess
from typing import Any

from hillm.contracts.device import DeviceResult


class UsbTransport:
    transport_id = "usb"

    def available(self) -> bool:
        return shutil.which("lsusb") is not None

    def connect(self, *, address: str, **options: Any) -> DeviceResult:
        return self.status(address=address, **options)

    def disconnect(self, *, address: str, **options: Any) -> DeviceResult:
        return DeviceResult(ok=True, backend=self.transport_id, message="usb scan session closed")

    def read(self, *, address: str, register: str = "", **options: Any) -> DeviceResult:
        if not self.available():
            return DeviceResult(ok=False, backend=self.transport_id, error="lsusb not available")
        try:
            proc = subprocess.run(["lsusb"], capture_output=True, text=True, check=False, timeout=10)
            lines = [line for line in proc.stdout.splitlines() if line.strip()]
            if register:
                lines = [line for line in lines if register.lower() in line.lower()]
            return DeviceResult(
                ok=proc.returncode == 0,
                backend=self.transport_id,
                value=lines,
                error=None if proc.returncode == 0 else proc.stderr.strip(),
            )
        except Exception as exc:
            return DeviceResult(ok=False, backend=self.transport_id, error=str(exc))

    def write(self, *, address: str, value: Any, register: str = "", **options: Any) -> DeviceResult:
        return DeviceResult(ok=False, backend=self.transport_id, error="usb write not supported")

    def actuate(self, *, address: str, action: str, **params: Any) -> DeviceResult:
        return self.read(address=address, register=action, **params)

    def status(self, *, address: str, **options: Any) -> DeviceResult:
        return self.read(address=address, **options)
