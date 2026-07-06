"""HILLM — Hardware Interface LLM."""

from __future__ import annotations

__version__ = "0.1.6"

__all__ = [
    "__version__",
    "actuate_device",
    "connect_device",
    "detect_devices",
    "disconnect_device",
    "ecosystem_status",
    "get_device_spec",
    "iter_device_specs",
    "read_device",
    "scan_host",
    "status_device",
    "write_device",
]


def __getattr__(name: str):
    if name in {
        "actuate_device",
        "connect_device",
        "disconnect_device",
        "read_device",
        "status_device",
        "write_device",
    }:
        from hillm import controller

        return getattr(controller, name)
    if name in {"detect_devices", "get_device_spec", "iter_device_specs"}:
        from hillm import registry

        return getattr(registry, name)
    if name == "ecosystem_status":
        from hillm.validation import ecosystem_status

        return ecosystem_status
    if name == "scan_host":
        from hillm.discovery.scan import scan_host

        return scan_host
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
