"""Declarative registry of hardware device profiles."""

from __future__ import annotations

import os
import shutil
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Literal

DeviceCategory = Literal[
    "display",
    "camera",
    "audio",
    "input",
    "usb",
    "serial",
    "fieldbus",
    "gpio",
    "network",
    "sensor",
    "actuator",
]
DeviceTransport = Literal[
    "dry_run",
    "serial",
    "modbus",
    "mqtt",
    "http",
    "v4l",
    "display",
    "audio",
    "input",
    "usb",
]
WhichFn = Callable[[str], str | None]

_SERIAL_PORT_CANDIDATES: tuple[str, ...] = (
    "/dev/ttyACM0",
    "/dev/ttyUSB0",
    "/dev/ttyUSB1",
    "/dev/ttyS0",
)


def first_existing_serial_path(*candidates: str) -> str:
    """Return the first existing serial device path, or empty string."""
    seen: set[str] = set()
    for path in candidates:
        if not path or path in seen:
            continue
        seen.add(path)
        if os.path.exists(path):
            return path
    return ""


@dataclass(frozen=True)
class DeviceSpec:
    id: str
    label: str
    category: DeviceCategory
    transport: DeviceTransport
    address: str = ""
    capabilities: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    detect_commands: tuple[str, ...] = ()
    detect_paths: tuple[str, ...] = ()
    env_vars: tuple[str, ...] = ()
    notes: str = ""
    default_register: str = ""

    def resolve_address(self, override: str | None = None) -> str:
        if override and override.strip():
            return override.strip()
        env_key = f"HILLM_{self.id.upper().replace('-', '_')}_ADDRESS"
        configured = os.environ.get(env_key, self.address).strip()
        if self.transport != "serial" or not configured or os.path.exists(configured):
            return configured
        fallback = first_existing_serial_path(configured, *self.detect_paths, *_SERIAL_PORT_CANDIDATES)
        return fallback or configured

    def missing_env_vars(self, environ: dict[str, str] | None = None) -> tuple[str, ...]:
        env = environ if environ is not None else os.environ
        return tuple(name for name in self.env_vars if not env.get(name, "").strip())

    def to_dict(
        self,
        *,
        which: WhichFn | None = None,
        environ: dict[str, str] | None = None,
        connected: bool | None = None,
    ) -> dict[str, object]:
        resolver = which or shutil.which
        detected = any(resolver(cmd) for cmd in self.detect_commands) or any(
            os.path.exists(path) for path in self.detect_paths
        )
        missing_env = self.missing_env_vars(environ)
        return {
            "id": self.id,
            "label": self.label,
            "category": self.category,
            "transport": self.transport,
            "address": self.resolve_address(),
            "capabilities": list(self.capabilities),
            "aliases": list(self.aliases),
            "detect_commands": list(self.detect_commands),
            "detect_paths": list(self.detect_paths),
            "notes": self.notes,
            "default_register": self.default_register,
            "detected": detected,
            "missing_env_vars": list(missing_env),
            "ready": detected and not missing_env,
            "connected": connected,
        }


_DEVICE_SPECS: tuple[DeviceSpec, ...] = (
    # Displays / HDMI
    DeviceSpec(
        id="display-primary",
        label="Primary display",
        category="display",
        transport="display",
        capabilities=("status", "brightness", "mode"),
        detect_commands=("xrandr", "wlr-randr"),
        notes="X11/Wayland display control via xrandr or wlr-randr.",
        aliases=("display",),
    ),
    DeviceSpec(
        id="hdmi-out",
        label="HDMI output",
        category="display",
        transport="display",
        address="HDMI-1",
        capabilities=("status", "mode", "power"),
        detect_commands=("xrandr",),
        aliases=("hdmi",),
    ),
    # Cameras
    DeviceSpec(
        id="camera-usb",
        label="USB camera",
        category="camera",
        transport="v4l",
        address="/dev/video0",
        capabilities=("capture", "status"),
        detect_paths=("/dev/video0",),
        aliases=("webcam", "camera"),
    ),
    # Audio
    DeviceSpec(
        id="microphone-default",
        label="Default microphone",
        category="audio",
        transport="audio",
        capabilities=("read", "status"),
        detect_commands=("pactl", "arecord"),
        aliases=("mic",),
    ),
    DeviceSpec(
        id="speaker-default",
        label="Default speaker",
        category="audio",
        transport="audio",
        capabilities=("write", "status"),
        detect_commands=("pactl", "aplay"),
        aliases=("speaker",),
    ),
    # Input
    DeviceSpec(
        id="keyboard-default",
        label="System keyboard",
        category="input",
        transport="input",
        capabilities=("status",),
        detect_paths=("/dev/input/by-id",),
        aliases=("keyboard",),
    ),
    DeviceSpec(
        id="mouse-default",
        label="System mouse",
        category="input",
        transport="input",
        capabilities=("status",),
        detect_paths=("/dev/input/by-id",),
        aliases=("mouse",),
    ),
    # USB
    DeviceSpec(
        id="usb-hub",
        label="USB devices",
        category="usb",
        transport="usb",
        capabilities=("list", "status"),
        detect_commands=("lsusb",),
        aliases=("usb",),
    ),
    # Serial / RS232 / RS485
    DeviceSpec(
        id="serial-ttyusb0",
        label="USB serial (ttyUSB0)",
        category="serial",
        transport="serial",
        address="/dev/ttyUSB0",
        capabilities=("read", "write", "connect"),
        detect_paths=("/dev/ttyUSB0",),
        aliases=("rs232", "rs485"),
    ),
    DeviceSpec(
        id="serial-ttyacm0",
        label="USB CDC serial (ttyACM0)",
        category="serial",
        transport="serial",
        address="/dev/ttyACM0",
        capabilities=("read", "write", "connect"),
        detect_paths=("/dev/ttyACM0",),
    ),
    # Fieldbus / Modbus
    DeviceSpec(
        id="modbus-rtu",
        label="Modbus RTU",
        category="fieldbus",
        transport="modbus",
        address="/dev/ttyUSB0",
        capabilities=("read", "write", "connect"),
        env_vars=("HILLM_MODBUS_PORT",),
        default_register="holding:0",
        aliases=("modbus",),
    ),
    DeviceSpec(
        id="modbus-tcp",
        label="Modbus TCP",
        category="fieldbus",
        transport="modbus",
        address="127.0.0.1:502",
        capabilities=("read", "write", "connect"),
        env_vars=("HILLM_MODBUS_HOST",),
        default_register="holding:0",
    ),
    # GPIO / sensors / actuators
    DeviceSpec(
        id="gpio-board",
        label="GPIO board",
        category="gpio",
        transport="dry_run",
        capabilities=("read", "write", "actuate"),
        notes="Platform-specific GPIO backend selected at runtime.",
    ),
    DeviceSpec(
        id="sensor-temp",
        label="Temperature sensor",
        category="sensor",
        transport="serial",
        address="/dev/ttyUSB0",
        capabilities=("read", "status"),
        detect_paths=("/dev/ttyACM0", "/dev/ttyUSB0"),
        default_register="temperature",
        aliases=("temp", "temperature"),
    ),
    DeviceSpec(
        id="actuator-relay",
        label="Relay actuator",
        category="actuator",
        transport="modbus",
        address="127.0.0.1:502",
        capabilities=("write", "actuate"),
        default_register="coil:0",
        aliases=("relay",),
    ),
    # Network devices
    DeviceSpec(
        id="mqtt-broker",
        label="MQTT broker",
        category="network",
        transport="mqtt",
        address="mqtt://127.0.0.1:1883",
        capabilities=("read", "write", "connect"),
        env_vars=("HILLM_MQTT_URL",),
        aliases=("mqtt",),
    ),
    DeviceSpec(
        id="http-device",
        label="HTTP REST device",
        category="network",
        transport="http",
        address="http://127.0.0.1:8080",
        capabilities=("read", "write", "status"),
        aliases=("rest-device",),
    ),
)

_ALIAS_INDEX: dict[str, str] = {}
for _spec in _DEVICE_SPECS:
    _ALIAS_INDEX[_spec.id] = _spec.id
    for _alias in _spec.aliases:
        _ALIAS_INDEX[_alias] = _spec.id


def normalize_device_id(raw: str) -> str:
    key = raw.strip().lower().replace(" ", "-")
    return _ALIAS_INDEX.get(key, key)


def iter_device_specs() -> tuple[DeviceSpec, ...]:
    return _DEVICE_SPECS


def get_device_spec(device_id: str) -> DeviceSpec | None:
    nid = normalize_device_id(device_id)
    for spec in _DEVICE_SPECS:
        if spec.id == nid:
            return spec
    return None


def suggest_device_ids(raw: str, *, limit: int = 5) -> list[str]:
    key = raw.strip().lower().replace(" ", "-")
    if not key:
        return []
    matches: list[str] = []
    for spec in _DEVICE_SPECS:
        candidates = (spec.id, spec.category, *spec.aliases)
        if any(key in candidate or candidate in key for candidate in candidates):
            matches.append(spec.id)
    return list(dict.fromkeys(matches))[:limit]


def format_unknown_device(raw: str) -> str:
    suggestions = suggest_device_ids(raw)
    if suggestions:
        return f"unknown device: {raw} (try: {', '.join(suggestions)})"
    return f"unknown device: {raw} (run: hillm devices)"


def detect_devices(
    *,
    category: str | None = None,
    project_hint_ids: Iterable[str] = (),
) -> list[dict[str, object]]:
    del project_hint_ids  # reserved for project-level overrides
    rows: list[dict[str, object]] = []
    for spec in _DEVICE_SPECS:
        if category and spec.category != category:
            continue
        rows.append(spec.to_dict())
    return rows
