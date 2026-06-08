"""Display / HDMI transport (xrandr / wlr-randr)."""

from __future__ import annotations

import shutil
import subprocess
from typing import Any

from hillm.contracts.device import DeviceResult


class DisplayTransport:
    transport_id = "display"

    def available(self) -> bool:
        return shutil.which("xrandr") is not None or shutil.which("wlr-randr") is not None

    def _run(self, command: list[str]) -> DeviceResult:
        try:
            proc = subprocess.run(command, capture_output=True, text=True, check=False, timeout=10)
            ok = proc.returncode == 0
            return DeviceResult(
                ok=ok,
                backend=self.transport_id,
                value=proc.stdout.strip(),
                message=proc.stderr.strip() or proc.stdout.strip(),
                error=None if ok else proc.stderr.strip() or f"exit {proc.returncode}",
                data={"command": command},
            )
        except Exception as exc:
            return DeviceResult(ok=False, backend=self.transport_id, error=str(exc))

    def connect(self, *, address: str, **options: Any) -> DeviceResult:
        return self.status(address=address, **options)

    def disconnect(self, *, address: str, **options: Any) -> DeviceResult:
        return DeviceResult(ok=True, backend=self.transport_id, message=f"display session closed: {address}")

    def read(self, *, address: str, register: str = "", **options: Any) -> DeviceResult:
        if shutil.which("xrandr"):
            return self._run(["xrandr", "--query"])
        if shutil.which("wlr-randr"):
            return self._run(["wlr-randr"])
        return DeviceResult(ok=False, backend=self.transport_id, error="no display tool in PATH (xrandr/wlr-randr)")

    def write(self, *, address: str, value: Any, register: str = "", **options: Any) -> DeviceResult:
        output = address or str(options.get("output", "HDMI-1"))
        mode = str(value)
        if shutil.which("xrandr"):
            return self._run(["xrandr", "--output", output, "--mode", mode])
        return DeviceResult(ok=False, backend=self.transport_id, error="xrandr required for display write")

    def actuate(self, *, address: str, action: str, **params: Any) -> DeviceResult:
        output = address or str(params.get("output", "HDMI-1"))
        if action in {"on", "enable"} and shutil.which("xrandr"):
            return self._run(["xrandr", "--output", output, "--auto"])
        if action in {"off", "disable"} and shutil.which("xrandr"):
            return self._run(["xrandr", "--output", output, "--off"])
        return DeviceResult(ok=False, backend=self.transport_id, error=f"unsupported display action: {action}")

    def status(self, *, address: str, **options: Any) -> DeviceResult:
        return self.read(address=address, **options)
