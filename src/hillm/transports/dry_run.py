"""Dry-run transport — always available, no hardware side effects."""

from __future__ import annotations

from typing import Any

from hillm.contracts.device import DeviceResult


class DryRunTransport:
    transport_id = "dry_run"

    def available(self) -> bool:
        return True

    def connect(self, *, address: str, **options: Any) -> DeviceResult:
        return DeviceResult(
            ok=True,
            backend=self.transport_id,
            message=f"dry-run connect {address}",
            data={"address": address, "options": options},
        )

    def disconnect(self, *, address: str, **options: Any) -> DeviceResult:
        return DeviceResult(
            ok=True,
            backend=self.transport_id,
            message=f"dry-run disconnect {address}",
            data={"address": address},
        )

    def read(self, *, address: str, register: str = "", **options: Any) -> DeviceResult:
        return DeviceResult(
            ok=True,
            backend=self.transport_id,
            value=f"dry:{register or 'value'}",
            message=f"dry-run read {address}",
            data={"address": address, "register": register, "options": options},
        )

    def write(self, *, address: str, value: Any, register: str = "", **options: Any) -> DeviceResult:
        return DeviceResult(
            ok=True,
            backend=self.transport_id,
            value=value,
            message=f"dry-run write {address}",
            data={"address": address, "register": register, "value": value},
        )

    def actuate(self, *, address: str, action: str, **params: Any) -> DeviceResult:
        return DeviceResult(
            ok=True,
            backend=self.transport_id,
            message=f"dry-run actuate {action} on {address}",
            data={"address": address, "action": action, "params": params},
        )

    def status(self, *, address: str, **options: Any) -> DeviceResult:
        return DeviceResult(
            ok=True,
            backend=self.transport_id,
            message="dry-run status ok",
            data={"address": address, "state": "simulated"},
        )
