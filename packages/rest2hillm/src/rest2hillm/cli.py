from __future__ import annotations

import argparse

import uvicorn

from rest2hillm.app import DEFAULT_PORT, create_app


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rest2hillm")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args(argv)
    uvicorn.run(create_app(), host=args.host, port=args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
