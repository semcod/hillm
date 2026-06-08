from __future__ import annotations

import shlex
from typing import Any


def _flag(rest: list[str], name: str) -> str | None:
    key = name.upper()
    upper = [token.upper() for token in rest]
    if key in upper:
        idx = upper.index(key)
        if idx + 1 < len(rest):
            return rest[idx + 1]
    return None


def _bool_flag(rest: list[str], name: str) -> bool | None:
    value = _flag(rest, name)
    if value is None:
        return None
    return value.lower() in {"1", "true", "yes", "on"}


def _device_payload(rest: list[str]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    device = _flag(rest, "DEVICE")
    if device:
        payload["device"] = device
    register = _flag(rest, "REGISTER")
    if register:
        payload["register"] = register
    address = _flag(rest, "ADDRESS")
    if address:
        payload["address"] = address
    value = _flag(rest, "VALUE")
    if value is not None:
        payload["value"] = value
    action = _flag(rest, "ACTION")
    if action:
        payload["action"] = action
    dry_run = _bool_flag(rest, "DRY_RUN")
    if dry_run is not None:
        payload["dry_run"] = dry_run
    category = _flag(rest, "CATEGORY")
    if category:
        payload["category"] = category
    prompt = _flag(rest, "PROMPT")
    if prompt:
        payload["prompt"] = prompt
    return payload


def parse_line(line: str, *, default_file: str | None = None) -> dict[str, Any]:
    del default_file
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return {}
    tokens = shlex.split(stripped)
    verb = tokens[0].upper()
    rest = tokens[1:]
    payload: dict[str, Any] = {"verb": verb}
    if verb in {"READ", "WRITE", "ACTUATE", "CONNECT", "DISCONNECT", "STATUS", "VALIDATE"}:
        payload.update(_device_payload(rest))
    elif verb == "DEVICES":
        category = _flag(rest, "CATEGORY")
        if category:
            payload["category"] = category
    elif verb == "RESOLVE":
        prompt = _flag(rest, "PROMPT")
        if prompt:
            payload["prompt"] = prompt
        elif rest:
            payload["prompt"] = " ".join(rest).strip('"')
    elif verb == "EXECUTE":
        action = _flag(rest, "ACTION") or "read"
        payload.update(_device_payload(rest))
        payload["action"] = action
    return payload
