"""Hardware driver contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class DeviceResult:
    ok: bool
    device_id: str = ""
    backend: str = ""
    value: Any = None
    message: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "device_id": self.device_id,
            "backend": self.backend,
            "value": self.value,
            "message": self.message,
            "data": self.data,
            "error": self.error,
        }


class HardwareTransport(Protocol):
    """Low-level transport for a device category."""

    transport_id: str

    def available(self) -> bool:
        """Return True when this transport can run on the current host."""

    def connect(self, *, address: str, **options: Any) -> DeviceResult:
        """Establish a session with the hardware endpoint."""

    def disconnect(self, *, address: str, **options: Any) -> DeviceResult:
        """Tear down a session."""

    def read(self, *, address: str, register: str = "", **options: Any) -> DeviceResult:
        """Read a value, register, or sensor channel."""

    def write(self, *, address: str, value: Any, register: str = "", **options: Any) -> DeviceResult:
        """Write a value to a register, GPIO pin, or control channel."""

    def actuate(self, *, address: str, action: str, **params: Any) -> DeviceResult:
        """Perform a higher-level action (move servo, switch relay, capture frame)."""

    def status(self, *, address: str, **options: Any) -> DeviceResult:
        """Return transport/device health information."""
