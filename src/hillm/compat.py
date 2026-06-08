"""Compatibility helpers for Koru / semcod ecosystem integration."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

from hillm.controller import actuate_device, connect_device, read_device, write_device
from hillm.registry import detect_devices, get_device_spec, iter_device_specs, normalize_device_id

HARDWARE_AUTOPILOT_BACKEND = "hillm_shell"
HARDWARE_BACKEND_PROFILE_ID = "hardware_device_cli"


def agent_backend_profiles() -> tuple[dict[str, object], ...]:
    return (
        {
            "id": HARDWARE_BACKEND_PROFILE_ID,
            "transport": "hillm hardware subprocess",
            "can_push_chat": False,
            "can_pull_chat_text": False,
            "needs_gui_session": False,
            "mcp_tools_only": False,
            "primary_code": "/home/tom/github/semcod/hillm",
        },
    )


def agent_backend_aliases() -> dict[str, str]:
    return {
        "hillm_shell": HARDWARE_BACKEND_PROFILE_ID,
        "hardware_cli": HARDWARE_BACKEND_PROFILE_ID,
        "device_cli": HARDWARE_BACKEND_PROFILE_ID,
    }


def is_hardware_device(device_id: str) -> bool:
    return get_device_spec(device_id) is not None


def tool_registry_entries() -> tuple[dict[str, object], ...]:
    entries: list[dict[str, object]] = []
    for spec in iter_device_specs():
        entries.append(
            {
                "id": spec.id,
                "name": spec.label,
                "category": "hardware",
                "lane": "native",
                "stability": "beta",
                "detect": {
                    "commands": list(spec.detect_commands),
                    "markers": list(spec.detect_paths),
                    "env": list(spec.env_vars),
                },
                "invoke": (
                    f"koru hillm read --device {spec.id} "
                    "--register '<register>'"
                ),
                "notes": f"Hardware lane via hillm ({spec.category}/{spec.transport}).",
            }
        )
    return tuple(entries)


def detect_koru_device_rows(*, project_hint_ids: Iterable[str] = ()) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in detect_devices(project_hint_ids=project_hint_ids):
        device_id = str(row["id"])
        label = str(row["label"])
        ready = bool(row.get("ready"))
        rows.append(
            {
                "id": device_id,
                "label": label,
                "available": ready,
                "launchable": ready,
                "autopilot_backend": HARDWARE_AUTOPILOT_BACKEND if ready else None,
                "reason": f"{label} hardware profile {'ready' if ready else 'not ready'}.",
                "category": row.get("category"),
                "transport": row.get("transport"),
            }
        )
    return rows


def drive_koru_hardware(
    *,
    device_id: str,
    action: str,
    project: Path,
    register: str = "",
    value: str | None = None,
    dry_run: bool = False,
) -> dict[str, object]:
    del project  # reserved for project-scoped device maps
    normalized = normalize_device_id(device_id)
    action_key = action.strip().lower()
    if action_key == "read":
        result = read_device(normalized, register=register or None, dry_run=dry_run)
    elif action_key == "write":
        result = write_device(normalized, value, register=register or None, dry_run=dry_run)
    elif action_key == "connect":
        result = connect_device(normalized, dry_run=dry_run)
    elif action_key == "actuate":
        result = actuate_device(normalized, value or register or "run", dry_run=dry_run)
    else:
        return {
            "ok": False,
            "backend": "hillm_shell",
            "device_id": normalized,
            "message": f"unsupported action: {action}",
            "type": "error",
        }
    payload = result.to_dict()
    payload["backend"] = "hillm_shell"
    payload["type"] = "ok" if result.ok else "error"
    return payload
