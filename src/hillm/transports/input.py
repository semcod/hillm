"""Keyboard / mouse input device transport."""

from __future__ import annotations

import os
from typing import Any

from hillm.contracts.device import DeviceResult


class InputTransport:
    transport_id = "input"

    def available(self) -> bool:
        return os.path.isdir("/dev/input")

    def connect(self, *, address: str, **options: Any) -> DeviceResult:
        return self.status(address=address, **options)

    def disconnect(self, *, address: str, **options: Any) -> DeviceResult:
        return DeviceResult(ok=True, backend=self.transport_id, message="input session closed")

    def read(self, *, address: str, register: str = "", **options: Any) -> DeviceResult:
        root = address or "/dev/input/by-id"
        if not os.path.isdir(root):
            return DeviceResult(ok=False, backend=self.transport_id, error=f"missing input path: {root}")
        entries = sorted(os.listdir(root))
        return DeviceResult(ok=True, backend=self.transport_id, value=entries, data={"path": root})

    def write(self, *, address: str, value: Any, register: str = "", **options: Any) -> DeviceResult:
        return DeviceResult(
            ok=False,
            backend=self.transport_id,
            error="direct input write is unsafe; use gillm injection lane",
        )

    def actuate(self, *, address: str, action: str, **params: Any) -> DeviceResult:
        return DeviceResult(
            ok=False,
            backend=self.transport_id,
            error="input actuation belongs to gillm; hillm only reports device presence",
        )

    def status(self, *, address: str, **options: Any) -> DeviceResult:
        return self.read(address=address or "/dev/input/by-id", **options)
