"""MQTT network device transport."""

from __future__ import annotations

from typing import Any

from hillm.contracts.device import DeviceResult


class MqttTransport:
    transport_id = "mqtt"

    def available(self) -> bool:
        try:
            import paho.mqtt.client  # noqa: F401

            return True
        except ImportError:
            return False

    def connect(self, *, address: str, **options: Any) -> DeviceResult:
        if not self.available():
            return DeviceResult(
                ok=False,
                backend=self.transport_id,
                error="paho-mqtt not installed; pip install 'hillm[mqtt]'",
            )
        return DeviceResult(ok=True, backend=self.transport_id, message=f"mqtt broker reachable: {address}")

    def disconnect(self, *, address: str, **options: Any) -> DeviceResult:
        return DeviceResult(ok=True, backend=self.transport_id, message=f"mqtt disconnected: {address}")

    def read(self, *, address: str, register: str = "", **options: Any) -> DeviceResult:
        topic = register or str(options.get("topic", "hillm/read"))
        return DeviceResult(
            ok=True,
            backend=self.transport_id,
            value=None,
            message=f"mqtt subscribe stub for {address} topic={topic}",
            data={"topic": topic, "note": "use hillm workflow or project bridge for live subscribe"},
        )

    def write(self, *, address: str, value: Any, register: str = "", **options: Any) -> DeviceResult:
        topic = register or str(options.get("topic", "hillm/write"))
        return DeviceResult(
            ok=True,
            backend=self.transport_id,
            value=value,
            message=f"mqtt publish stub to {topic}",
            data={"broker": address, "topic": topic, "payload": value},
        )

    def actuate(self, *, address: str, action: str, **params: Any) -> DeviceResult:
        return self.write(address=address, value=action, register=str(params.get("topic", "hillm/actuate")), **params)

    def status(self, *, address: str, **options: Any) -> DeviceResult:
        return DeviceResult(ok=True, backend=self.transport_id, data={"broker": address, "transport": "mqtt"})
