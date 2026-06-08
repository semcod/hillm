"""HTTP REST hardware gateway transport."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from hillm.contracts.device import DeviceResult


class HttpDeviceTransport:
    transport_id = "http"

    def available(self) -> bool:
        return True

    def _request(self, url: str, *, method: str = "GET", body: Any = None, timeout: float = 5.0) -> DeviceResult:
        data = None
        headers = {"Accept": "application/json"}
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read().decode("utf-8", errors="replace")
            try:
                value = json.loads(raw)
            except json.JSONDecodeError:
                value = raw
            return DeviceResult(ok=True, backend=self.transport_id, value=value, data={"url": url})
        except urllib.error.URLError as exc:
            return DeviceResult(ok=False, backend=self.transport_id, error=str(exc), data={"url": url})

    def connect(self, *, address: str, **options: Any) -> DeviceResult:
        return self.status(address=address, **options)

    def disconnect(self, *, address: str, **options: Any) -> DeviceResult:
        return DeviceResult(ok=True, backend=self.transport_id, message=f"http session closed: {address}")

    def read(self, *, address: str, register: str = "", **options: Any) -> DeviceResult:
        path = register or str(options.get("path", "/status"))
        url = address.rstrip("/") + (path if path.startswith("/") else f"/{path}")
        return self._request(url, method="GET", timeout=float(options.get("timeout", 5.0)))

    def write(self, *, address: str, value: Any, register: str = "", **options: Any) -> DeviceResult:
        path = register or str(options.get("path", "/write"))
        url = address.rstrip("/") + (path if path.startswith("/") else f"/{path}")
        return self._request(url, method="POST", body={"value": value}, timeout=float(options.get("timeout", 5.0)))

    def actuate(self, *, address: str, action: str, **params: Any) -> DeviceResult:
        path = str(params.get("path", f"/actuate/{action}"))
        return self.write(address=address, value=params, register=path, **params)

    def status(self, *, address: str, **options: Any) -> DeviceResult:
        return self.read(address=address, register="/health", **options)
