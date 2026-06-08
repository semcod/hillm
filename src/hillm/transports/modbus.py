"""Modbus RTU/TCP transport."""

from __future__ import annotations

from typing import Any

from hillm.contracts.device import DeviceResult


def _parse_register(register: str) -> tuple[str, int]:
    if ":" in register:
        kind, raw = register.split(":", 1)
        return kind.strip().lower(), int(raw)
    return "holding", int(register)


class ModbusTransport:
    transport_id = "modbus"

    def available(self) -> bool:
        try:
            import pymodbus  # noqa: F401

            return True
        except ImportError:
            return False

    def _client(self, address: str, **options: Any):
        from pymodbus.client import ModbusSerialClient, ModbusTcpClient

        if address.startswith("/dev/"):
            return ModbusSerialClient(
                port=address,
                baudrate=int(options.get("baudrate", 9600)),
            )
        host, _, port = address.partition(":")
        return ModbusTcpClient(host=host, port=int(port or 502))

    def connect(self, *, address: str, **options: Any) -> DeviceResult:
        if not self.available():
            return DeviceResult(
                ok=False,
                backend=self.transport_id,
                error="pymodbus not installed; pip install 'hillm[modbus]'",
            )
        try:
            client = self._client(address, **options)
            ok = bool(client.connect())
            client.close()
            return DeviceResult(
                ok=ok,
                backend=self.transport_id,
                message=f"modbus connect {address}",
                error=None if ok else f"modbus connect failed: {address}",
            )
        except Exception as exc:
            return DeviceResult(ok=False, backend=self.transport_id, error=str(exc))

    def disconnect(self, *, address: str, **options: Any) -> DeviceResult:
        return DeviceResult(ok=True, backend=self.transport_id, message=f"modbus disconnected: {address}")

    def read(self, *, address: str, register: str = "holding:0", **options: Any) -> DeviceResult:
        if not self.available():
            return DeviceResult(ok=False, backend=self.transport_id, error="pymodbus not installed")
        kind, index = _parse_register(register)
        unit = int(options.get("unit", 1))
        try:
            client = self._client(address, **options)
            if not client.connect():
                return DeviceResult(ok=False, backend=self.transport_id, error=f"connect failed: {address}")
            if kind == "coil":
                response = client.read_coils(index, count=1, slave=unit)
            elif kind == "input":
                response = client.read_input_registers(index, count=1, slave=unit)
            else:
                response = client.read_holding_registers(index, count=1, slave=unit)
            client.close()
            if response.isError():
                return DeviceResult(ok=False, backend=self.transport_id, error=str(response))
            value = response.bits[0] if kind == "coil" else response.registers[0]
            return DeviceResult(ok=True, backend=self.transport_id, value=value, data={"register": register})
        except Exception as exc:
            return DeviceResult(ok=False, backend=self.transport_id, error=str(exc))

    def write(self, *, address: str, value: Any, register: str = "holding:0", **options: Any) -> DeviceResult:
        if not self.available():
            return DeviceResult(ok=False, backend=self.transport_id, error="pymodbus not installed")
        kind, index = _parse_register(register)
        unit = int(options.get("unit", 1))
        try:
            client = self._client(address, **options)
            if not client.connect():
                return DeviceResult(ok=False, backend=self.transport_id, error=f"connect failed: {address}")
            if kind == "coil":
                response = client.write_coil(index, bool(value), slave=unit)
            else:
                response = client.write_register(index, int(value), slave=unit)
            client.close()
            if response.isError():
                return DeviceResult(ok=False, backend=self.transport_id, error=str(response))
            return DeviceResult(ok=True, backend=self.transport_id, value=value, data={"register": register})
        except Exception as exc:
            return DeviceResult(ok=False, backend=self.transport_id, error=str(exc))

    def actuate(self, *, address: str, action: str, **params: Any) -> DeviceResult:
        register = str(params.get("register", "coil:0"))
        value = params.get("value", action.lower() in {"on", "true", "1", "open"})
        return self.write(address=address, value=value, register=register, **params)

    def status(self, *, address: str, **options: Any) -> DeviceResult:
        return self.connect(address=address, **options)
