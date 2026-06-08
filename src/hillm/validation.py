"""Validation hooks for HILLM ecosystem integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from hillm.discovery.scan import scan_host
from hillm.registry import detect_devices, get_device_spec, iter_device_specs
from hillm.transports.base import get_transport


HILLM_DRIVE_ACTIONS = frozenset(
    {"hillm.read", "hillm.write", "hillm.actuate", "hillm.connect", "hardware_drive"},
)
HILLM_INTENT_CONTRACTS = (
    (
        "# @intract.v1 id:hillm.hardware_drive scope:block "
        "intent:drive:hardware domain:hardware "
        "input:device,action output:hardware_result effect:device "
        "validate:known_device,action_presence,allowed_action "
        'meaning:"validate hardware drive intent before execution"'
    ),
)


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    device_id: str
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "device_id": self.device_id,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }


def validate_device_readiness(device_id: str, *, action: str = "read") -> ValidationResult:
    spec = get_device_spec(device_id)
    if spec is None:
        return ValidationResult(ok=False, device_id=device_id, errors=(f"unknown device: {device_id}",))
    errors: list[str] = []
    warnings: list[str] = []
    missing_env = spec.missing_env_vars()
    if missing_env:
        errors.append(f"missing env: {', '.join(missing_env)}")
    if action not in spec.capabilities and action != "status":
        warnings.append(f"action {action!r} not listed in capabilities {spec.capabilities}")
    try:
        backend = get_transport(spec.transport)
        if not backend.available():
            warnings.append(f"transport {spec.transport!r} not available on host; dry-run still works")
    except ValueError as exc:
        errors.append(str(exc))
    return ValidationResult(ok=not errors, device_id=spec.id, errors=tuple(errors), warnings=tuple(warnings))


def ecosystem_status() -> dict[str, Any]:
    devices = detect_devices()
    ready = sum(1 for row in devices if row.get("ready"))
    return {
        "ok": True,
        "package": "hillm",
        "devices_registered": len(list(iter_device_specs())),
        "devices_detected": sum(1 for row in devices if row.get("detected")),
        "devices_ready": ready,
        "contracts": list(HILLM_INTENT_CONTRACTS),
        "expected_actions": sorted(HILLM_DRIVE_ACTIONS),
        "scan": scan_host(),
    }


def intent_contracts() -> tuple[str, ...]:
    return HILLM_INTENT_CONTRACTS
