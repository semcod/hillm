"""Video4Linux camera transport."""

from __future__ import annotations

import os
from typing import Any

from hillm.contracts.device import DeviceResult


class V4lTransport:
    transport_id = "v4l"

    def available(self) -> bool:
        return os.path.isdir("/dev") and any(name.startswith("video") for name in os.listdir("/dev"))

    def connect(self, *, address: str, **options: Any) -> DeviceResult:
        exists = os.path.exists(address)
        return DeviceResult(
            ok=exists,
            backend=self.transport_id,
            message=f"v4l device {'found' if exists else 'missing'}: {address}",
            error=None if exists else f"missing camera device: {address}",
        )

    def disconnect(self, *, address: str, **options: Any) -> DeviceResult:
        return DeviceResult(ok=True, backend=self.transport_id, message=f"v4l released: {address}")

    def read(self, *, address: str, register: str = "", **options: Any) -> DeviceResult:
        return self.actuate(address=address, action="capture", register=register, **options)

    def write(self, *, address: str, value: Any, register: str = "", **options: Any) -> DeviceResult:
        return DeviceResult(
            ok=False,
            backend=self.transport_id,
            error="v4l devices are read-only; use ACTUATE capture",
        )

    def actuate(self, *, address: str, action: str, **params: Any) -> DeviceResult:
        if action not in {"capture", "snapshot"}:
            return DeviceResult(ok=False, backend=self.transport_id, error=f"unsupported camera action: {action}")
        output = str(params.get("output", f"{address.replace('/', '_')}.jpg"))
        return DeviceResult(
            ok=True,
            backend=self.transport_id,
            message=f"v4l capture planned for {address}",
            data={
                "device": address,
                "output": output,
                "note": "install ffmpeg or opencv bridge for live capture",
            },
        )

    def status(self, *, address: str, **options: Any) -> DeviceResult:
        return self.connect(address=address, **options)
