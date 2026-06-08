"""Audio input/output transport (PulseAudio / ALSA)."""

from __future__ import annotations

import shutil
import subprocess
from typing import Any

from hillm.contracts.device import DeviceResult


class AudioTransport:
    transport_id = "audio"

    def available(self) -> bool:
        return any(shutil.which(cmd) for cmd in ("pactl", "arecord", "aplay"))

    def _run(self, command: list[str]) -> DeviceResult:
        try:
            proc = subprocess.run(command, capture_output=True, text=True, check=False, timeout=10)
            ok = proc.returncode == 0
            return DeviceResult(
                ok=ok,
                backend=self.transport_id,
                value=proc.stdout.strip(),
                error=None if ok else proc.stderr.strip() or f"exit {proc.returncode}",
            )
        except Exception as exc:
            return DeviceResult(ok=False, backend=self.transport_id, error=str(exc))

    def connect(self, *, address: str, **options: Any) -> DeviceResult:
        return self.status(address=address, **options)

    def disconnect(self, *, address: str, **options: Any) -> DeviceResult:
        return DeviceResult(ok=True, backend=self.transport_id, message="audio session closed")

    def read(self, *, address: str, register: str = "", **options: Any) -> DeviceResult:
        if shutil.which("pactl"):
            return self._run(["pactl", "list", "sources", "short"])
        return DeviceResult(ok=False, backend=self.transport_id, error="pactl not available")

    def write(self, *, address: str, value: Any, register: str = "", **options: Any) -> DeviceResult:
        if shutil.which("pactl") and str(value).isdigit():
            return self._run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", str(value)])
        return DeviceResult(
            ok=True,
            backend=self.transport_id,
            message="audio write stub",
            data={"address": address, "value": value},
        )

    def actuate(self, *, address: str, action: str, **params: Any) -> DeviceResult:
        if action == "mute" and shutil.which("pactl"):
            return self._run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "1"])
        if action == "unmute" and shutil.which("pactl"):
            return self._run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "0"])
        return DeviceResult(ok=False, backend=self.transport_id, error=f"unsupported audio action: {action}")

    def status(self, *, address: str, **options: Any) -> DeviceResult:
        if shutil.which("pactl"):
            return self._run(["pactl", "info"])
        return DeviceResult(ok=False, backend=self.transport_id, error="pactl not available")
