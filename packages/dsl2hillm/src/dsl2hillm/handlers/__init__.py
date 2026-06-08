from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class HandlerResult:
    ok: bool
    output: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "output": self.output, "data": self.data, "error": self.error}


def run_query(payload: dict[str, Any], *, workdir: Path) -> HandlerResult:
    del workdir
    verb = str(payload["verb"]).upper()
    if verb == "HEALTH":
        return _health()
    if verb == "DEVICES":
        return _devices(payload)
    if verb == "ORIENT":
        return _orient()
    if verb == "ACTIONS":
        return _actions()
    if verb == "VALIDATE":
        return _validate(payload)
    if verb == "READ":
        return _read(payload)
    if verb == "STATUS":
        return _status(payload)
    if verb == "RESOLVE":
        return _resolve(payload)
    return HandlerResult(ok=False, error=f"unknown query verb: {verb}")


def run_command(payload: dict[str, Any], *, workdir: Path) -> HandlerResult:
    del workdir
    verb = str(payload["verb"]).upper()
    if verb == "WRITE":
        return _write(payload)
    if verb == "ACTUATE":
        return _actuate(payload)
    if verb == "CONNECT":
        return _connect(payload)
    if verb == "DISCONNECT":
        return _disconnect(payload)
    if verb == "EXECUTE":
        return _execute(payload)
    return HandlerResult(ok=False, error=f"unknown command verb: {verb}")


def _health() -> HandlerResult:
    from hillm.validation import ecosystem_status

    data = ecosystem_status()
    return HandlerResult(ok=True, output=json.dumps(data, indent=2), data=data)


def _devices(payload: dict[str, Any]) -> HandlerResult:
    from hillm.registry import detect_devices

    rows = detect_devices(category=payload.get("category"))
    return HandlerResult(ok=True, output=json.dumps(rows, indent=2), data={"devices": rows})


def _orient() -> HandlerResult:
    from hillm.discovery.scan import scan_host

    data = scan_host()
    return HandlerResult(ok=True, output=json.dumps(data, indent=2), data=data)


def _actions() -> HandlerResult:
    from hillm.validation import HILLM_DRIVE_ACTIONS

    data = {
        "actions": sorted(HILLM_DRIVE_ACTIONS),
        "verbs": sorted(["READ", "WRITE", "ACTUATE", "CONNECT", "DISCONNECT", "STATUS"]),
    }
    return HandlerResult(ok=True, output=json.dumps(data, indent=2), data=data)


def _validate(payload: dict[str, Any]) -> HandlerResult:
    from hillm.validation import ecosystem_status, validate_device_readiness

    device = payload.get("device")
    if device:
        result = validate_device_readiness(str(device), action=str(payload.get("action", "read")))
        data = result.to_dict()
        return HandlerResult(ok=result.ok, output=json.dumps(data, indent=2), data=data, error=data["errors"][0] if data["errors"] else None)
    data = ecosystem_status()
    return HandlerResult(ok=True, output=json.dumps(data, indent=2), data=data)


def _read(payload: dict[str, Any]) -> HandlerResult:
    from hillm.controller import read_device

    result = read_device(
        str(payload["device"]),
        register=str(payload.get("register", "")) or None,
        address=str(payload.get("address", "")) or None,
        dry_run=bool(payload.get("dry_run", False)),
    )
    data = result.to_dict()
    return HandlerResult(ok=result.ok, output=json.dumps(data, indent=2), data=data, error=result.error)


def _status(payload: dict[str, Any]) -> HandlerResult:
    from hillm.controller import status_device

    result = status_device(
        str(payload["device"]),
        address=str(payload.get("address", "")) or None,
        dry_run=bool(payload.get("dry_run", False)),
    )
    data = result.to_dict()
    return HandlerResult(ok=result.ok, output=json.dumps(data, indent=2), data=data, error=result.error)


def _write(payload: dict[str, Any]) -> HandlerResult:
    from hillm.controller import write_device

    result = write_device(
        str(payload["device"]),
        payload.get("value"),
        register=str(payload.get("register", "")) or None,
        address=str(payload.get("address", "")) or None,
        dry_run=bool(payload.get("dry_run", False)),
    )
    data = result.to_dict()
    return HandlerResult(ok=result.ok, output=json.dumps(data, indent=2), data=data, error=result.error)


def _actuate(payload: dict[str, Any]) -> HandlerResult:
    from hillm.controller import actuate_device

    result = actuate_device(
        str(payload["device"]),
        str(payload.get("action", "run")),
        address=str(payload.get("address", "")) or None,
        dry_run=bool(payload.get("dry_run", False)),
    )
    data = result.to_dict()
    return HandlerResult(ok=result.ok, output=json.dumps(data, indent=2), data=data, error=result.error)


def _connect(payload: dict[str, Any]) -> HandlerResult:
    from hillm.controller import connect_device

    result = connect_device(
        str(payload["device"]),
        address=str(payload.get("address", "")) or None,
        dry_run=bool(payload.get("dry_run", False)),
    )
    data = result.to_dict()
    return HandlerResult(ok=result.ok, output=json.dumps(data, indent=2), data=data, error=result.error)


def _disconnect(payload: dict[str, Any]) -> HandlerResult:
    from hillm.controller import disconnect_device

    result = disconnect_device(
        str(payload["device"]),
        address=str(payload.get("address", "")) or None,
        dry_run=bool(payload.get("dry_run", False)),
    )
    data = result.to_dict()
    return HandlerResult(ok=result.ok, output=json.dumps(data, indent=2), data=data, error=result.error)


def _execute(payload: dict[str, Any]) -> HandlerResult:
    from hillm.controller import HardwareRequest, execute_request

    result = execute_request(
        HardwareRequest(
            device_id=str(payload["device"]),
            action=str(payload.get("action", "read")),
            address=str(payload.get("address", "")),
            register=str(payload.get("register", "")),
            value=payload.get("value"),
            dry_run=bool(payload.get("dry_run", False)),
        )
    )
    data = result.to_dict()
    return HandlerResult(ok=result.ok, output=json.dumps(data, indent=2), data=data, error=result.error)


def _resolve(payload: dict[str, Any]) -> HandlerResult:
    prompt = str(payload.get("prompt", ""))
    try:
        from nlp2hillm.to_dsl import to_dsl

        line = to_dsl(prompt)
    except ImportError:
        return HandlerResult(ok=False, error="nlp2hillm not installed")
    except Exception as exc:
        return HandlerResult(ok=False, error=str(exc))
    return HandlerResult(ok=True, output=line, data={"dsl": line, "prompt": prompt})
