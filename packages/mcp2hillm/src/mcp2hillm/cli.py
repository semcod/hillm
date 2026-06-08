from __future__ import annotations

import argparse

from mcp2hillm.server import mcp


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="mcp2hillm")
    parser.add_argument("mode", nargs="?", default="stdio", choices=["stdio"])
    args = parser.parse_args(argv)
    if args.mode == "stdio":
        mcp.run(transport="stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
